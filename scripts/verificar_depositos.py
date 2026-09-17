#!/usr/bin/env python3
"""
Verificação quinzenal (dias 1 e 16) dos depósitos a prazo do comparador LF.

O que faz:
 1. Descarrega o Excel mais recente do Economia e Finanças e lê todas as linhas.
 2. Compara as TANB do Excel com data/depositos.json (banco + produto + prazo).
 3. Vai à página de cada banco (campo "url" e "url_fin" de cada depósito), guarda o
    texto e lista as percentagens encontradas perto do nome do produto.
 4. Escreve verificacao/AAAA-MM/relatorio.md com as diferenças e o que falta ler à mão.

O script NUNCA altera data/depositos.json. A alteração é feita depois da aprovação
do Franklin (ver verificacao/TAREFA.md).

Uso:
    pip install requests openpyxl beautifulsoup4 pypdf
    python3 scripts/verificar_depositos.py            # mês corrente
    python3 scripts/verificar_depositos.py --sem-bancos   # só o Excel (mais rápido)
"""
import argparse
import hashlib
import datetime as dt
import difflib
import io
import json
import re
import sys
import unicodedata
from pathlib import Path

import requests

try:
    import openpyxl
except ImportError:
    openpyxl = None
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "depositos.json"
EF_PAGE = "https://economiafinancas.com/taxas-de-juro-depositos-a-prazo/"
FORUM_POST = "https://forumdoinvestidor.pt/viewtopic.php?p=4319#p4319"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.7"}
TIMEOUT = 30

# Nomes que os bancos usam noutras fontes -> nome no nosso JSON
ALIASES = {
    "banco big": "Banco BiG", "big": "Banco BiG",
    "activobank": "ActivoBank",
    "banco portugues de gestao": "Banco Português de Gestão", "bpg": "Banco Português de Gestão",
    "best": "Banco Best", "banco best": "Banco Best",
    "banco carregosa": "Banco Carregosa", "carregosa": "Banco Carregosa",
    "haitong": "Haitong Bank", "haitong bank portugal": "Haitong Bank", "haitong bank": "Haitong Bank",
    "bai europa": "BAI Europa", "banco bai europa": "BAI Europa",
    "invest": "Banco Invest", "banco invest": "Banco Invest",
    "klarna": "Klarna",
    "finantia": "Banco Finantia", "banco finantia": "Banco Finantia",
    "atlantico": "Atlântico Europa", "banco atlantico europa": "Atlântico Europa", "atlantico europa": "Atlântico Europa",
    "open bank": "Openbank", "openbank": "Openbank",
    "bankinter": "Bankinter",
    "bni europa": "BNI Europa", "bni": "BNI Europa",
    "banco ctt": "Banco CTT",
    "bison bank": "Bison Bank", "bison": "Bison Bank",
}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9 ]+", " ", s.lower()).strip()


def banco_canon(nome):
    n = norm(nome)
    if n in ALIASES:
        return ALIASES[n]
    for k, v in ALIASES.items():
        if k in n:
            return v
    return nome


def pct(v):
    """'2,75', '2.75%', 0.0275 -> 2.75"""
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return round(v * 100, 3) if v < 1 else round(float(v), 3)
    m = re.search(r"(\d+)[.,](\d+)", str(v))
    if not m:
        m = re.search(r"(\d+)", str(v))
        return float(m.group(1)) if m else None
    return round(float(m.group(1) + "." + m.group(2)), 3)


def meses(prazo, unidade):
    """(1, 'ano(s)') -> 12; (92, 'dias') -> 3; (6, 'meses') -> 6"""
    p = pct(prazo)
    if p is None:
        return None
    u = norm(unidade)
    if "ano" in u:
        return int(round(p * 12))
    if "dia" in u:
        return int(round(p / 30.4))
    return int(round(p))


# ---------------------------------------------------------------- Excel EF
def excel_url():
    r = requests.get(EF_PAGE, headers=UA, timeout=TIMEOUT)
    r.raise_for_status()
    # link "Melhores Taxas de Juro de Depósitos a Prazo <Mês> <Ano> (EXCEL)"
    hrefs = re.findall(r'href="([^"]+)"[^>]*>[^<]*EXCEL', r.text, flags=re.I)
    if not hrefs:
        hrefs = re.findall(r'href="([^"]+\.xlsx?)"', r.text, flags=re.I)
    if not hrefs:
        raise RuntimeError("Não encontrei o link do Excel em " + EF_PAGE)
    return hrefs[0]


def ler_excel():
    if openpyxl is None:
        raise RuntimeError("pip install openpyxl")
    url = excel_url()
    r = requests.get(url, headers=UA, timeout=TIMEOUT, allow_redirects=True)
    r.raise_for_status()
    wb = openpyxl.load_workbook(io.BytesIO(r.content), data_only=True, read_only=True)
    linhas, headers_vistos = [], {}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        # encontrar a linha de cabeçalho: a que tem "banco" e algo com "tanb" ou "bruta"
        hi = None
        for i, row in enumerate(rows[:40]):
            cells = [norm(c) for c in row]
            if any("banco" in c for c in cells) and any(("tanb" in c or "bruta" in c) for c in cells):
                hi = i
                break
        if hi is None:
            continue
        hdr = [norm(c) for c in rows[hi]]
        headers_vistos[ws.title] = hdr

        def col(*keys):
            for k in keys:
                for j, h in enumerate(hdr):
                    if k in h:
                        return j
            return None

        c_banco, c_prod = col("banco"), col("deposito", "nome", "produto")
        c_tanb = col("tanb", "bruta")
        c_prazo, c_unid = col("prazo"), col("dias", "unid", "meses")
        c_min = col("minimo", "min")
        c_pen = col("penal", "mobil")
        c_fin = col("fin", "ligacao", "link")
        c_data = col("data", "consult")
        for row in rows[hi + 1:]:
            if row is None or c_banco is None or not row[c_banco]:
                continue
            tanb = pct(row[c_tanb]) if c_tanb is not None else None
            if tanb is None:
                continue
            linhas.append({
                "folha": ws.title,
                "banco": banco_canon(row[c_banco]),
                "banco_original": str(row[c_banco]),
                "produto": str(row[c_prod]) if c_prod is not None and row[c_prod] else "",
                "tanb": tanb,
                "meses": meses(row[c_prazo], row[c_unid] if c_unid is not None else "meses") if c_prazo is not None else None,
                "minimo": row[c_min] if c_min is not None else None,
                "penalizacao": row[c_pen] if c_pen is not None else None,
                "fin": row[c_fin] if c_fin is not None else None,
                "data": str(row[c_data]) if c_data is not None and row[c_data] else None,
            })
    return url, linhas, headers_vistos


# ---------------------------------------------------------------- páginas dos bancos
def texto_url(url):
    r = requests.get(url, headers=UA, timeout=TIMEOUT)
    r.raise_for_status()
    ct = r.headers.get("content-type", "")
    if "pdf" in ct or url.lower().endswith(".pdf"):
        if PdfReader is None:
            return "[pypdf não instalado]"
        return "\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(r.content)).pages)
    if BeautifulSoup is None:
        return re.sub(r"<[^>]+>", " ", r.text)
    soup = BeautifulSoup(r.text, "html.parser")
    for t in soup(["script", "style", "nav", "footer", "noscript"]):
        t.decompose()
    return re.sub(r"\n{3,}", "\n\n", soup.get_text("\n"))


def percentagens_perto(texto, produto, janela=400):
    """Devolve as percentagens que aparecem até `janela` caracteres depois do nome do produto."""
    achados = []
    chave = norm(produto).split()
    chave = [w for w in chave if len(w) > 3][:3]  # palavras mais distintivas
    tn = norm(texto)
    for w in chave:
        for m in re.finditer(re.escape(w), tn):
            trecho = texto[max(0, m.start() - 50): m.start() + janela]
            achados += re.findall(r"\d{1,2}[.,]\d{2}\s?%", trecho)
    return sorted(set(a.replace(" ", "") for a in achados))


# ---------------------------------------------------------------- comparação
def semelhanca(a, b):
    """Parecença entre nomes de produto; 'com' vs 'sem' mobilização conta como produto diferente."""
    na, nb = norm(a), norm(b)
    r = difflib.SequenceMatcher(None, na, nb).ratio()
    for w in ("com", "sem", "nao", "novos"):
        if ((" " + w + " ") in " " + na + " ") != ((" " + w + " ") in " " + nb + " "):
            r -= 0.3
    return max(r, 0)


def comparar(deps, linhas):
    diffs, iguais, sem_match = [], [], []
    for d in deps:
        cand = [l for l in linhas if l["banco"] == d["banco"]]
        for m, info in d["prazos"].items():
            m = int(m)
            mesmo_prazo = [l for l in cand if l["meses"] == m]
            if not mesmo_prazo:
                sem_match.append(f"{d['banco']} · {d['produto']} · {m}m (nenhuma linha do Excel com este banco e prazo)")
                continue
            # produto mais parecido
            best = max(mesmo_prazo, key=lambda l: semelhanca(l["produto"], d["produto"]))
            score = semelhanca(best["produto"], d["produto"])
            item = {"id": d["id"], "banco": d["banco"], "produto": d["produto"], "meses": m,
                    "nosso": info["tanb"], "excel": best["tanb"], "excel_produto": best["produto"],
                    "score": round(score, 2), "penalizacao": best["penalizacao"], "fin": best["fin"]}
            if score < 0.55:
                sem_match.append(f"{d['banco']} · {d['produto']} · {m}m (o mais parecido no Excel é \"{best['produto']}\" a {best['tanb']:.2f}%, confiança {score:.2f})")
            elif abs(item["nosso"] - item["excel"]) >= 0.005:
                diffs.append(item)
            else:
                iguais.append(item)
    return diffs, iguais, sem_match


def novidades(deps, linhas, minimo=1.0):
    nossos = {d["banco"] for d in deps}
    out = []
    for l in linhas:
        if l["tanb"] >= minimo and l["banco"] not in nossos:
            out.append(l)
        elif l["tanb"] >= 2.5 and l["banco"] in nossos:
            # produto do banco que não temos (score baixo com todos os nossos)
            prods = [norm(d["produto"]) for d in deps if d["banco"] == l["banco"]]
            if prods and max(semelhanca(l["produto"], p) for p in prods) < 0.45:
                out.append(l)
    return out


# ---------------------------------------------------------------- relatório
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sem-bancos", action="store_true", help="não visitar as páginas dos bancos")
    ap.add_argument("--mes", default=dt.date.today().strftime("%Y-%m-%d"), help="pasta do relatório (por defeito a data de hoje)")
    args = ap.parse_args()

    dados = json.loads(DATA.read_text(encoding="utf-8"))
    deps = dados["depositos"]
    outdir = ROOT / "verificacao" / args.mes
    (outdir / "paginas").mkdir(parents=True, exist_ok=True)

    rel = [f"# Verificação dos depósitos a prazo - {args.mes}", "",
           f"Gerado a {dt.date.today().isoformat()}. Base: data/depositos.json verificado a {dados['meta']['data_verificacao']}.", ""]

    # 1) Excel
    try:
        url, linhas, hdrs = ler_excel()
        rel += [f"## 1. Economia e Finanças", "", f"Excel lido: {url} ({len(linhas)} linhas com TANB).", ""]
        (outdir / "economiafinancas.json").write_text(json.dumps(linhas, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
        diffs, iguais, sem_match = comparar(deps, linhas)
        rel += ["### Taxas diferentes das nossas", ""]
        if diffs:
            rel += ["| Depósito | Prazo | Nossa | Excel | Produto no Excel | Confiança |", "|---|---|---|---|---|---|"]
            for x in sorted(diffs, key=lambda x: -abs(x["nosso"] - x["excel"])):
                rel.append(f"| {x['banco']} · {x['produto']} | {x['meses']}m | {x['nosso']:.2f}% | **{x['excel']:.2f}%** | {x['excel_produto']} | {x['score']} |")
        else:
            rel.append("Nenhuma. Todas as taxas que o Excel cobre batem certo.")
        rel += ["", f"### Iguais: {len(iguais)} taxas confirmadas", ""]
        if sem_match:
            rel += ["### Sem correspondência no Excel (confirmar no banco)", ""] + [f"- {s}" for s in sem_match] + [""]
        nov = novidades(deps, linhas)
        if nov:
            rel += ["### Ofertas no Excel que não temos (TANB >= 1,00%)", "",
                    "| Banco | Produto | Prazo | TANB | Mínimo |", "|---|---|---|---|---|"]
            for l in sorted(nov, key=lambda l: -l["tanb"]):
                rel.append(f"| {l['banco']} | {l['produto']} | {l['meses']}m | {l['tanb']:.2f}% | {l['minimo'] or ''} |")
            rel.append("")
    except Exception as e:  # noqa
        rel += ["## 1. Economia e Finanças", "", f"FALHOU: {e}", "Verificar à mão em " + EF_PAGE, ""]

    # 2) Páginas dos bancos
    rel += ["## 2. Páginas dos bancos", ""]
    if args.sem_bancos:
        rel.append("Saltado (--sem-bancos).")
    else:
        vistos = {}
        for d in deps:
            for campo in ("url", "url_fin"):
                u = d.get(campo)
                if not u or u.startswith("#") or "literaciafinanceira.pt" in u:
                    continue
                if u not in vistos:
                    try:
                        vistos[u] = texto_url(u)
                        nome = re.sub(r"[^a-z0-9]+", "-", norm(u))[:70] + "-" + hashlib.md5(u.encode()).hexdigest()[:6] + ".txt"
                        (outdir / "paginas" / nome).write_text(vistos[u], encoding="utf-8")
                    except Exception as e:  # noqa
                        vistos[u] = None
                        rel.append(f"- ❌ {d['banco']} · {d['produto']}: não consegui abrir {u} ({e})")
                        continue
                txt = vistos[u]
                if txt is None:
                    continue
                pcts = percentagens_perto(txt, d["produto"])
                nossas = ", ".join(f"{int(m)}m {i['tanb']:.2f}%" for m, i in d["prazos"].items())
                flag = "" if all(f"{i['tanb']:.2f}".replace(".", ",") + "%" in pcts for i in d["prazos"].values()) else " ⚠️"
                rel.append(f"- {d['banco']} · {d['produto']} ({campo}){flag}: temos {nossas}; na página perto do nome aparecem {', '.join(pcts) or 'nenhuma percentagem'}")
        rel += ["", "⚠️ = pelo menos uma das nossas taxas não aparece perto do nome do produto: ler o texto guardado em `paginas/` ou a FIN.", ""]

    # 2b) Catálogos dos bancos: descobrir depósitos novos
    rel += ["## 2b. Catálogos dos bancos (depósitos novos?)", ""]
    if args.sem_bancos:
        rel.append("Saltado (--sem-bancos).")
    else:
        conhecidos = {norm(d["produto"]) for d in deps}
        for banco, url in dados.get("catalogos", {}).items():
            try:
                txt = texto_url(url)
                (outdir / "paginas" / ("catalogo-" + re.sub(r"[^a-z0-9]+", "-", norm(banco)) + ".txt")).write_text(txt, encoding="utf-8")
            except Exception as e:  # noqa
                rel.append(f"- ❌ {banco}: não consegui abrir {url} ({e})")
                continue
            # candidatos: linhas curtas com "depósito"/"DP" e uma percentagem por perto
            cands = set()
            for linha in txt.splitlines():
                l = linha.strip()
                if 6 <= len(l) <= 90 and re.search(r"dep[oó]sito|\bDP\b|poupan[cç]a a prazo", l, flags=re.I):
                    if norm(l) not in conhecidos and not any(k in norm(l) for k in conhecidos if len(k) > 8):
                        cands.add(l)
            pcts = sorted(set(re.findall(r"\d{1,2}[.,]\d{2}\s?%", txt)))
            rel.append(f"- {banco}: {len(cands)} nome(s) que não temos" + (": " + "; ".join(sorted(cands)[:8]) if cands else "") + f" · percentagens na página: {', '.join(pcts[:12]) or 'nenhuma'}")
        rel += ["", "Lista de candidatos, não de novidades confirmadas: abrir a página guardada em `paginas/catalogo-*.txt` para cada nome novo com taxa >= 1,00% e verificar se é um depósito a prazo para particulares.", ""]

    # 3) Fórum
    rel += ["## 3. Fórum do Investidor (JRJordao)", "",
            f"A tabela é uma imagem e o fórum bloqueia pedidos automáticos. Abrir {FORUM_POST}, ver a data da última atualização e comparar com a tabela acima. Serve de terceira verificação e apanha mudanças que os sites ainda não mostram.", ""]

    # 4) A confirmar
    pend = [d for d in deps if d.get("a_confirmar") or not d.get("url_fin")]
    rel += ["## 4. Pendentes no nosso JSON", ""]
    rel += [f"- {d['banco']} · {d['produto']}: " + ("; ".join(n for n in d["notas"] if "A CONFIRMAR" in n) or "falta url_fin") for d in pend]
    rel += ["", "## Próximo passo", "",
            "Rever este relatório, confirmar cada diferença na FIN e só depois editar data/depositos.json (campo meta.data_verificacao incluído). O script não altera dados."]

    (outdir / "relatorio.md").write_text("\n".join(rel), encoding="utf-8")
    print("\n".join(rel))
    print(f"\nRelatório em {outdir / 'relatorio.md'}")


if __name__ == "__main__":
    sys.exit(main())
