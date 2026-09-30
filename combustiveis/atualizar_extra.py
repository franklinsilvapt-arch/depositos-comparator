#!/usr/bin/env python3
"""Atualiza combustiveis/extra.json.

1. Preco medio por marca: API publica da DGEG (precoscombustiveis.dgeg.gov.pt),
   media simples dos precos afixados por posto, marcas com 20 ou mais postos.
2. Preco eficiente: relatorio semanal da ERSE (PDF). Tenta ler o PDF mais recente;
   se a leitura falhar, mantem os valores que ja estavam no ficheiro.

Dependencia opcional: pypdf (so para o ponto 2).
"""
import io, json, os, re, sys, urllib.parse, urllib.request
from datetime import date

OUT = os.path.join(os.path.dirname(__file__), "extra.json")
UA = {"User-Agent": "Mozilla/5.0 (compatible; LF-combustiveis/1.0; +https://www.literaciafinanceira.pt)"}
DGEG = ("https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/PesquisarPostos?idsTiposComb={id}"
        "&idMarca=&idTipoPosto=&idDistrito=&idsMunicipios=&qtdPorPagina=6000&pagina=1")
ERSE_LISTA = "https://www.erse.pt/combustiveis-e-gpl/supervisao-do-mercado/supervisao-dos-precos-de-combustiveis/"
MIN_POSTOS = 20


def get(url):
    partes = urllib.parse.urlsplit(url)
    url = urllib.parse.urlunsplit(partes._replace(path=urllib.parse.quote(partes.path, safe="/%")))
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
        return r.read()


def marcas(id_comb):
    dados = json.loads(get(DGEG.format(id=id_comb)).decode("utf-8-sig"))
    por_marca, todos = {}, []
    for p in dados.get("resultado") or []:
        try:
            preco = float(str(p["Preco"]).replace("€", "").replace(",", ".").strip())
        except (ValueError, KeyError):
            continue
        if not 0.5 < preco < 4:
            continue
        todos.append(preco)
        por_marca.setdefault((p.get("Marca") or "").strip(), []).append(preco)
    if len(todos) < 1000:
        raise RuntimeError(f"DGEG devolveu so {len(todos)} postos para {id_comb}")
    lista = sorted(([m, len(v), round(sum(v) / len(v), 4)] for m, v in por_marca.items() if m and len(v) >= MIN_POSTOS),
                   key=lambda x: x[2])
    return {"media": round(sum(todos) / len(todos), 4), "postos": len(todos), "lista": lista}


def n(s):
    return float(s.replace(",", "."))


def eficiente():
    """Le o relatorio semanal mais recente da ERSE. Devolve None se algo nao bater certo."""
    from pypdf import PdfReader
    html = get(ERSE_LISTA).decode("utf-8", errors="replace")
    m = re.search(r'href="([^"]+relat[^"]*semanal[^"]*\.pdf)"[^>]*>\s*Semana de ([^<]+?)\s*<', html, re.I)
    if not m:
        return None
    url = urllib.parse.urljoin(ERSE_LISTA, m.group(1))
    semana = re.sub(r"\s+de (\w+) a ", r" a ", m.group(2).strip(), count=1) if m.group(2).count(" de ") == 2 and \
        m.group(2).split(" de ")[1].split(" ")[0] == m.group(2).split(" de ")[2].split(" ")[0] else m.group(2).strip()
    txt = " ".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(get(url))).pages)
    txt = re.sub(r"\s+", " ", txt)
    a = re.search(r"antes de impostos é de (\d,\d{3}) €/l para a gasolina 95 simples e de (\d,\d{3}) €/l para o gasóleo", txt)
    b = re.search(r"situa-se em (\d,\d{3}) €/l na gasolina 95 simples e em (\d,\d{3}) €/l no gasóleo", txt)
    if not a or not b:
        return None
    out = {"semana": semana, "fonte": url,
           "gasolina": {"pvp": n(b.group(1)), "semImpostos": n(a.group(1))},
           "gasoleo": {"pvp": n(b.group(2)), "semImpostos": n(a.group(2))}}
    if not (1 < out["gasolina"]["pvp"] < 4 and 1 < out["gasoleo"]["pvp"] < 4):
        return None
    return out


def main():
    with open(OUT, encoding="utf-8") as f:
        dados = json.load(f)
    hoje = date.today().isoformat()
    dados["marcas"] = {"data": hoje, "minPostos": MIN_POSTOS, "gasolina": marcas(3201), "gasoleo": marcas(2101)}
    try:
        novo = eficiente()
        if novo and novo["fonte"] != dados.get("eficiente", {}).get("fonte"):
            # As comparacoes com a semana anterior (portico e descontos) sao preenchidas a mao: ficam de fora ate serem revistas.
            dados["eficiente"] = novo
            print("Preco eficiente atualizado:", novo["semana"])
    except Exception as e:  # o bloco da ERSE nunca deve impedir a atualizacao das marcas
        print("Preco eficiente: leitura falhou, mantidos os valores anteriores:", e, file=sys.stderr)
    dados["atualizado"] = hoje
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)
    print("Marcas:", len(dados["marcas"]["gasolina"]["lista"]), "gasolina,", len(dados["marcas"]["gasoleo"]["lista"]), "gasoleo")


if __name__ == "__main__":
    main()
