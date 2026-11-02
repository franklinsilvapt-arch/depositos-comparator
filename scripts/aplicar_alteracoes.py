#!/usr/bin/env python3
"""Aplica um ou mais ficheiros de alterações a data/depositos.json.

Existe porque o ficheiro de dados tem ~100 KB e não é prático reescrevê-lo
inteiro a cada ronda. Em vez disso escreve-se um patch pequeno em
verificacao/<AAAA-MM-DD>/alteracoes.json e isto aplica-o.

Formato do patch (todas as secções são opcionais):

{
  "data_verificacao": "2026-11-01",
  "taxas":      [{"id":"haitong-sem","prazo":"6","de":2.85,"para":2.90}],
  "campos":     [{"id":"best-novos","campo":"url_fin","de":"...","para":"..."}],
  "notas_add":  [{"id":"haitong-sem","texto":"..."}],
  "notas_sub":  [{"id":"klarna-fixo","antigo":"...","novo":"..."}],
  "novos":      [ {entrada completa, com todos os campos obrigatórios} ],
  "remover":    [{"id":"bpg-start","porque":"produto saiu do site"}]
}

O campo "de" é obrigatório em taxas e campos: se o valor atual não for esse,
o script pára. Isso impede que um patch escrito a partir de dados velhos
sobreponha silenciosamente uma alteração mais recente.

RONDA COMPLETA NUM SÓ FICHEIRO. Uma ronda costuma dar vários patches, e
dispará-los um a um à mão é trabalho repetido. Um ficheiro de ronda é um
patch cuja única secção é "patches", com a lista por ordem de aplicação:

{
  "patches": ["alteracoes.json", "alteracoes-taxas.json", "alteracoes-fins.json"]
}

Os caminhos são relativos à pasta do próprio ficheiro de ronda (ou absolutos
a partir da raiz do repositório, se começarem por "verificacao/"). Aplica-se
tudo em memória e só se grava no fim: se um único patch falhar o guard do
"de", nada é gravado. Assim uma ronda inteira entra com um dispatch só.

Uso:  python3 scripts/aplicar_alteracoes.py verificacao/2026-11-01/ronda.json
      python3 scripts/aplicar_alteracoes.py verificacao/2026-11-01/alteracoes.json
      python3 scripts/aplicar_alteracoes.py <patch> [<patch> ...] --dry-run
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DADOS = ROOT / "data/depositos.json"

SECCOES = ("data_verificacao", "taxas", "campos", "notas_add", "notas_sub",
           "novos", "remover", "patches")


def resolver(caminho, vistos=None):
    """Devolve a lista de patches a aplicar, por ordem, expandindo rondas."""
    vistos = vistos if vistos is not None else []
    cam = Path(caminho)
    if not cam.exists():
        cam2 = ROOT / caminho
        if cam2.exists():
            cam = cam2
    if not cam.exists():
        print("não existe o ficheiro %s" % caminho); sys.exit(2)
    cam = cam.resolve()
    if cam in vistos:
        print("ronda circular: %s aparece duas vezes" % cam); sys.exit(2)
    p = json.loads(cam.read_text(encoding="utf-8"))
    desconhecidas = [k for k in p if k not in SECCOES and not k.startswith("_")]
    if desconhecidas:
        print("secções desconhecidas em %s: %s" % (cam.name, ", ".join(desconhecidas)))
        sys.exit(2)
    if "patches" not in p:
        return [(cam, p)]
    outras = [k for k in p if k in SECCOES and k != "patches"]
    if outras:
        print("%s tem \"patches\" e também %s. Um ficheiro de ronda só lista patches."
              % (cam.name, ", ".join(outras)))
        sys.exit(2)
    fora = []
    for sub in p["patches"]:
        alvo = cam.parent / sub if not str(sub).startswith("verificacao/") else ROOT / sub
        fora += resolver(alvo, vistos + [cam])
    return fora


def rotulo(cam):
    """Caminho para mostrar: relativo à raiz do repositório quando der."""
    try:
        return cam.relative_to(ROOT)
    except ValueError:
        return cam


def aplicar(d, by, p, feito, falhas):
    def exige(cond, msg):
        if not cond: falhas.append(msg)
        return cond

    for t in p.get("taxas", []):
        i, pr = t["id"], str(t["prazo"])
        if not exige(i in by, "taxas: id desconhecido %s" % i): continue
        if not exige(pr in by[i]["prazos"], "taxas: %s não tem prazo de %s meses" % (i, pr)): continue
        atual = by[i]["prazos"][pr]["tanb"]
        if not exige(atual == t["de"], "taxas: %s %sm está a %s e o patch esperava %s" % (i, pr, atual, t["de"])): continue
        by[i]["prazos"][pr]["tanb"] = t["para"]
        feito.append("taxa   %-28s %2sm  %s -> %s" % (i, pr, atual, t["para"]))

    for c in p.get("campos", []):
        i, k = c["id"], c["campo"]
        if not exige(i in by, "campos: id desconhecido %s" % i): continue
        atual = by[i].get(k)
        if not exige(atual == c["de"], "campos: %s.%s está %r e o patch esperava %r" % (i, k, atual, c["de"])): continue
        by[i][k] = c["para"]
        feito.append("campo  %-28s %s" % (i, k))

    for n in p.get("notas_sub", []):
        i = n["id"]
        if not exige(i in by, "notas_sub: id desconhecido %s" % i): continue
        alvo = [j for j, x in enumerate(by[i]["notas"]) if n["antigo"] in x]
        if not exige(len(alvo) == 1, "notas_sub: %s tem %d notas com esse texto, esperava 1" % (i, len(alvo))): continue
        by[i]["notas"][alvo[0]] = by[i]["notas"][alvo[0]].replace(n["antigo"], n["novo"])
        feito.append("nota   %-28s substituída" % i)

    for n in p.get("notas_add", []):
        i = n["id"]
        if not exige(i in by, "notas_add: id desconhecido %s" % i): continue
        if n["texto"] in by[i]["notas"]:
            feito.append("nota   %-28s já existia, ignorada" % i); continue
        by[i]["notas"].append(n["texto"])
        feito.append("nota+  %-28s acrescentada" % i)

    for e in p.get("novos", []):
        if not exige(e["id"] not in by, "novos: id %s já existe" % e["id"]): continue
        d["depositos"].append(e); by[e["id"]] = e
        feito.append("novo   %-28s %s" % (e["id"], e.get("produto", "")))

    for r in p.get("remover", []):
        i = r["id"] if isinstance(r, dict) else r
        if not exige(i in by, "remover: id desconhecido %s" % i): continue
        d["depositos"] = [x for x in d["depositos"] if x["id"] != i]
        del by[i]
        feito.append("remove %-28s %s" % (i, (r.get("porque", "") if isinstance(r, dict) else "")))

    if "data_verificacao" in p:
        d["meta"]["data_verificacao"] = p["data_verificacao"]
        feito.append("meta   data_verificacao -> %s" % p["data_verificacao"])


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if not args:
        print("falta o caminho do ficheiro de alterações"); sys.exit(2)

    lista = []
    for a in args:
        lista += resolver(a)

    d = json.loads(DADOS.read_text(encoding="utf-8"))
    by = {e["id"]: e for e in d["depositos"]}
    falhas, total = [], 0

    for cam, p in lista:
        feito = []
        aplicar(d, by, p, feito, falhas)
        print("Patch: %s" % rotulo(cam))
        for f in feito: print("  ", f)
        print("   %d alterações.\n" % len(feito))
        total += len(feito)

    if len(lista) > 1:
        print("%d patches, %d alterações no total." % (len(lista), total))
    else:
        print("%d alterações aplicadas." % total)

    if falhas:
        print("\nNADA FOI GRAVADO. %d problemas:" % len(falhas))
        for f in falhas: print("  ", f)
        sys.exit(1)

    if dry:
        print("\n--dry-run: nada gravado."); sys.exit(0)

    DADOS.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n%s gravado com %d depósitos." % (DADOS, len(d["depositos"])))


if __name__ == "__main__":
    main()
