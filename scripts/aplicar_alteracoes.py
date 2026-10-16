#!/usr/bin/env python3
"""Aplica um ficheiro de alterações pequeno a data/depositos.json.

Existe porque o ficheiro de dados tem ~85 KB e não é prático reescrevê-lo
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

Uso:  python3 scripts/aplicar_alteracoes.py verificacao/2026-11-01/alteracoes.json
      python3 scripts/aplicar_alteracoes.py <patch> --dry-run
"""
import json, sys, io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DADOS = ROOT / "data/depositos.json"

if len(sys.argv) < 2:
    print("falta o caminho do ficheiro de alterações"); sys.exit(2)
PATCH = Path(sys.argv[1])
DRY = "--dry-run" in sys.argv

d = json.loads(DADOS.read_text(encoding="utf-8"))
p = json.loads(PATCH.read_text(encoding="utf-8"))
by = {e["id"]: e for e in d["depositos"]}
feito, falhas = [], []

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

print("Patch: %s" % PATCH)
for f in feito: print("  ", f)
print("\n%d alterações aplicadas." % len(feito))

if falhas:
    print("\nNADA FOI GRAVADO. %d problemas:" % len(falhas))
    for f in falhas: print("  ", f)
    sys.exit(1)

if DRY:
    print("\n--dry-run: nada gravado."); sys.exit(0)

DADOS.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("\n%s gravado com %d depósitos." % (DADOS, len(d["depositos"])))
