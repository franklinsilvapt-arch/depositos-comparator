#!/usr/bin/env python3
"""Verifica as taxas dos depósitos contra os preçários em PDF dos bancos.

Porque existe: o verificar_depositos.py lê páginas HTML e a maioria dos bancos
portugueses bloqueia leitura automática. Na verificação de 2026-11-01 falharam
BiG, Best, Carregosa, BAI, Invest, Haitong, Montepio, BPI, Novo Banco e
Santander. Os preçários em PDF dos mesmos bancos abriram sem problema, e são
documento vinculativo com data de entrada em vigor impressa, o que é melhor
fonte do que uma página de marketing.

A Parte I (comissões e despesas) e a Parte II (taxas de juro) estão dentro do
mesmo PDF: no ActivoBank a Parte II começa na página 40 de 62. Não há segundo
ficheiro a procurar. E lê-se com pdftotext, não por fetch de página: o fetch
devolve só os primeiros ~39 mil caracteres em texto verdadeiro e resume o resto,
e o resumo chega a dizer que a secção 17.2 não existe quando ela está lá.

O que faz:
  1. Descarrega o preçário de cada banco em data/precarios.json
  2. Lê a data de entrada em vigor. Se for igual à da última corrida, salta o
     banco: o documento não mudou, não há nada a comparar
  3. Extrai a secção dos depósitos a prazo e, para cada produto declarado,
     as linhas de prazo e taxa
  4. Compara com data/depositos.json e escreve:
       verificacao/<data>/precarios.md         relatório legível
       verificacao/<data>/alteracoes.json      patch para aplicar_alteracoes.py
     O patch só leva diferenças de taxa em produtos já existentes, cada uma com
     o valor antigo como guarda. Produtos novos e desaparecidos vão para o
     relatório como propostas, nunca para o patch: entrar ou sair da lista é
     decisão de uma pessoa

O que NAO faz: não altera data/depositos.json e não inventa correspondências.
A ligação entre o nome no preçário e o id do nosso ficheiro é declarada à mão
em data/precarios.json.

Uso:
  python3 scripts/verificar_precarios.py
  python3 scripts/verificar_precarios.py --banco "Banco BiG"
  python3 scripts/verificar_precarios.py --explorar <url> --formato carregosa
  python3 scripts/verificar_precarios.py --pdf-local /caminho/x.pdf --banco "Banco BiG"
"""
import argparse, datetime as dt, json, re, subprocess, sys, tempfile, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DADOS = ROOT / "data/depositos.json"
FONTES = ROOT / "data/precarios.json"
GRELHA = {"3", "6", "12", "24"}
UA = "Mozilla/5.0 (compatible; literaciafinanceira-verificador/1.0; +https://www.literaciafinanceira.pt)"

MESES_PT = {"jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
            "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12}


def baixar(url, destino):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf,*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        destino.write_bytes(r.read())


def texto_do_pdf(caminho):
    """pdftotext -layout preserva as colunas, que é o que faz as tabelas legíveis."""
    try:
        return subprocess.run(["pdftotext", "-layout", str(caminho), "-"],
                              capture_output=True, text=True, check=True, timeout=120).stdout
    except FileNotFoundError:
        sys.exit("falta o pdftotext. No Ubuntu: apt-get install -y poppler-utils")


RX_VIGOR = re.compile(
    r"[Ee]ntrada em vigor:?\s*(\d{1,2})\s*[-/ ]\s*([a-zç]{3,10}|\d{1,2})\s*[-/ ]\s*(\d{4})", re.I)


def _norm_data(m):
    dia, mes, ano = m.group(1), m.group(2).lower()[:3], m.group(3)
    n = MESES_PT.get(mes, mes if mes.isdigit() else None)
    return None if n is None else "%02d-%02d-%s" % (int(dia), int(n), ano)


def data_em_vigor(texto, antes_de=None):
    """Data de entrada em vigor do folheto.

    Um preçário traz várias: o Folheto de Comissões e o de Taxas de Juro têm
    datas diferentes, e cada página repete a sua no cabeçalho. A que vale para
    as taxas é a do cabeçalho da página onde a secção está, por isso, quando se
    sabe onde a secção começa, usa-se a última data antes dela.
    """
    achadas = [(m.start(), _norm_data(m)) for m in RX_VIGOR.finditer(texto)]
    achadas = [(i, d) for i, d in achadas if d]
    if not achadas:
        return None
    if antes_de is not None:
        anteriores = [d for i, d in achadas if i <= antes_de]
        if anteriores:
            return anteriores[-1]
    return achadas[0][1]


def rx_titulo(t):
    """Regex de um título tolerante a quebras de linha.

    O pdftotext parte títulos longos em duas linhas, por exemplo
    'Depósito a Prazo Novos\nMontantes'. Comparar a string literal falhava
    nesses casos e o produto parecia ter desaparecido do preçário.
    """
    return re.compile(r"\s+".join(re.escape(w) for w in t.split()), re.I)


RX_OUTRA_SECCAO = re.compile(r"\b(?!17\.2)\d{1,2}\.\d\.")


def inicio_seccao(texto, marca):
    """Posição onde a secção dos depósitos a prazo começa, ou None.

    Salta o índice: nestes preçários a primeira ocorrência de '17.2. Depósitos
    a prazo' está no índice, numa linha que traz também outras secções ao lado,
    por exemplo '19.2. Depósitos a prazo'. Apanhar essa levava a cortar o
    documento no sítio errado e, pior, a ler a data de entrada em vigor de
    outro folheto.
    """
    cands = [m.start() for m in re.finditer(re.escape(marca), texto, re.I)]
    if not cands:
        cands = [m.start() for m in re.finditer(r"17\.2\.?\s*Dep[óo]sitos a prazo", texto, re.I)]
    for i in cands:
        ini_linha = texto.rfind("\n", 0, i) + 1
        linha = texto[ini_linha:texto.find("\n", i)]
        if RX_OUTRA_SECCAO.search(linha):
            continue          # linha de índice
        return i
    return cands[0] if cands else None


def recortar_seccao(texto, marca):
    """Da secção até ao fim do documento.

    Não corta no fim da secção de propósito: em vários preçários a tabela
    continua em páginas seguintes sob 'continuação', e cortar cedo perdia
    produtos. Os títulos declarados delimitam o que interessa.
    """
    i = inicio_seccao(texto, marca)
    return None if i is None else texto[i:]


def so_coluna(texto, largura):
    """Corta cada linha à largura da coluna do nome e da taxa.

    O pdftotext -layout põe lado a lado a coluna do produto e a das condições.
    Um nome longo parte-se em duas linhas e, no meio, fica texto da coluna da
    direita, o que impede qualquer correspondência pelo nome completo. Cortar
    à largura da primeira coluna volta a juntar o nome.
    """
    if not largura:
        return texto
    return "\n".join(l[:largura].rstrip() for l in texto.split("\n"))


def blocos(seccao, titulos):
    """Parte a secção nos títulos declarados. Devolve {titulo: texto do bloco}."""
    marcas = []
    for t in titulos:
        for m in rx_titulo(t).finditer(seccao):
            # Só conta se o título abrir a linha. No Carregosa há referências
            # cruzadas a meio de linha, por exemplo "Máximo: Dobro do aplicado
            # no Depósito a Prazo Carregosa NextGen Welcome Boost", que de
            # outro modo cortavam o bloco do produto anterior antes da taxa.
            ini_linha = seccao.rfind("\n", 0, m.start()) + 1
            if seccao[ini_linha:m.start()].strip():
                continue
            marcas.append((m.start(), t))
    marcas.sort()
    out = {}
    for k, (ini, t) in enumerate(marcas):
        fim = marcas[k + 1][0] if k + 1 < len(marcas) else len(seccao)
        out.setdefault(t, "")
        out[t] += seccao[ini:fim]
    return out


# Vários preçários escrevem o prazo em dias (90 dias, 180 dias, 365 dias). Só se
# aceita um número de dias que caia claramente num prazo da grelha: 90 dias é o
# trimestre, 180 o semestre, e por aí. Um intervalo como "15 a 366 dias" não tem
# prazo nenhum da grelha e é ignorado de propósito, em vez de arredondado.
DIAS_PARA_MESES = ((83, 100, "3"), (170, 200, "6"), (355, 375, "12"), (720, 740, "24"))


def prazo_de_dias(n):
    for lo, hi, meses in DIAS_PARA_MESES:
        if lo <= n <= hi:
            return meses
    return None


def na_grelha_ou_longo(pr):
    """A grelha, mais os prazos em anos certos acima dos 2 anos.

    O comparador só deixa escolher até 2 anos, mas a tabela "Taxas por prazo" do
    detalhe mostra também os prazos mais longos (regra do Franklin, 2 nov 2026),
    por isso o verificador tem de os ver no preçário. Um prazo esquisito dentro
    dos 2 anos, como 18 meses, continua a ser ignorado: não tem onde aparecer.
    """
    if pr in GRELHA:
        return True
    n = int(pr)
    return n > 24 and n % 12 == 0


def taxas_do_bloco(bloco, regex, prazo_fixo=None):
    """Devolve {prazo_em_meses: taxa_float} a partir das linhas do bloco."""
    res = {}
    for m in re.finditer(regex, bloco, re.M):
        g = m.groupdict()
        taxa = float(g["taxa"].replace(",", "."))
        if prazo_fixo:
            pr = str(prazo_fixo)
        else:
            n, unidade = int(g["n"]), (g.get("unidade") or "meses").lower()
            if unidade.startswith("dia"):
                pr = prazo_de_dias(n)
                if pr is None:
                    continue
            elif unidade.startswith("ano"):
                pr = str(n * 12)
            else:
                pr = str(n)
        if na_grelha_ou_longo(pr) and taxa > 0:
            res.setdefault(pr, taxa)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--banco")
    ap.add_argument("--explorar", metavar="URL")
    ap.add_argument("--formato", default="carregosa")
    ap.add_argument("--pdf-local")
    ap.add_argument("--data", default=dt.date.today().isoformat())
    args = ap.parse_args()

    fontes = json.loads(FONTES.read_text(encoding="utf-8"))
    formatos = fontes["formatos"]

    if args.explorar:
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "p.pdf"
            baixar(args.explorar, p)
            txt = texto_do_pdf(p)
        print("entrada em vigor:", data_em_vigor(txt))  # documento inteiro, sem secção
        rx = formatos[args.formato]["linha"]
        print("\nlinhas de taxa que o parser '%s' vê:" % args.formato)
        for m in re.finditer(rx, txt, re.M):
            print("  ", m.group(0).strip())
        return 0

    dados = json.loads(DADOS.read_text(encoding="utf-8"))
    por_id = {e["id"]: e for e in dados["depositos"]}

    linhas, taxas_patch, falhas, propostas = [], [], [], []

    for banco in fontes["bancos"]:
        nome = banco["banco"]
        if args.banco and args.banco != nome:
            continue
        linhas.append("\n### %s" % nome)
        try:
            if args.pdf_local:
                txt = texto_do_pdf(Path(args.pdf_local))
            else:
                with tempfile.TemporaryDirectory() as td:
                    p = Path(td) / "p.pdf"
                    baixar(banco["url"], p)
                    txt = texto_do_pdf(p)
        except Exception as e:
            falhas.append("%s: não consegui abrir %s (%s)" % (nome, banco["url"], e))
            linhas.append("- NÃO ABRIU: %s" % e)
            continue

        inicio = inicio_seccao(txt, banco["seccao"])
        vigor = data_em_vigor(txt, antes_de=inicio)
        linhas.append("- preçário em vigor a %s (tínhamos visto %s)" % (vigor or "data não encontrada", banco["vigor_visto"]))
        if vigor and vigor == banco["vigor_visto"]:
            linhas.append("- documento igual ao da última corrida, nada a comparar")
            continue

        seccao = recortar_seccao(txt, banco["seccao"])
        if not seccao:
            falhas.append("%s: não encontrei a secção %r no PDF" % (nome, banco["seccao"]))
            linhas.append("- NÃO ENCONTREI A SECÇÃO %r" % banco["seccao"])
            continue

        fmt = formatos[banco["formato"]]
        seccao = so_coluna(seccao, fmt.get("largura"))
        titulos = [p["titulo"] for p in banco["produtos"]] + banco.get("ignorar_titulos", [])
        blocos_por_titulo = blocos(seccao, titulos)

        vistos = set()
        for prod in banco["produtos"]:
            t, pid = prod["titulo"], prod["id"]
            bloco = blocos_por_titulo.get(t)
            if bloco is None:
                linhas.append("- %s: título não encontrado no preçário. Pode ter mudado de nome ou saído" % t)
                propostas.append("%s · %s: deixou de aparecer no preçário, confirmar se saiu" % (nome, t))
                continue
            achadas = taxas_do_bloco(bloco, fmt["linha"], prod.get("prazo"))
            if not achadas:
                linhas.append("- %s: bloco encontrado mas sem linhas de taxa legíveis" % t)
                falhas.append("%s · %s: bloco sem taxas legíveis" % (nome, t))
                continue
            vistos.add(pid)
            e = por_id.get(pid)
            if e is None:
                linhas.append("- %s: %s. Não temos nenhuma entrada com o id %r" % (t, achadas, pid))
                propostas.append("%s · %s: %s, candidato a acrescentar (id %s não existe)" % (nome, t, achadas, pid))
                continue
            for pr, taxa in sorted(achadas.items(), key=lambda x: int(x[0])):
                nosso = (e["prazos"].get(pr) or {}).get("tanb")
                if nosso is None:
                    linhas.append("- %s %sm: preçário diz %s e não temos esse prazo" % (t, pr, taxa))
                    propostas.append("%s · %s: prazo de %s meses a %s%% que não temos" % (nome, t, pr, taxa))
                elif abs(nosso - taxa) > 1e-9:
                    linhas.append("- **%s %sm: %s -> %s**" % (t, pr, nosso, taxa))
                    taxas_patch.append({"id": pid, "prazo": pr, "de": nosso, "para": taxa,
                                        "_fonte": "%s, preçário em vigor a %s" % (nome, vigor)})
                else:
                    linhas.append("- %s %sm: %s, igual" % (t, pr, taxa))

        nossos_do_banco = {i for i, e in por_id.items() if e["banco"] == nome}
        for i in sorted(nossos_do_banco - vistos):
            linhas.append("- %s: temos esta entrada e o preçário não a confirmou nesta corrida" % i)

    hoje = args.data
    destino = ROOT / "verificacao" / hoje
    destino.mkdir(parents=True, exist_ok=True)

    rel = ["# Verificação por preçário - %s" % hoje, "",
           "Fonte: os preçários em PDF declarados em `data/precarios.json`. Este relatório não altera dados.", ""]
    if taxas_patch:
        rel += ["## Taxas que mudaram", ""] + ["- `%s` %sm: %s para %s (%s)" % (t["id"], t["prazo"], t["de"], t["para"], t["_fonte"]) for t in taxas_patch] + [""]
    else:
        rel += ["## Taxas que mudaram", "", "Nenhuma.", ""]
    if propostas:
        rel += ["## Propostas que precisam de decisão", "",
                "Não entram no patch. Acrescentar ou remover um produto é decisão de uma pessoa.", ""] + ["- %s" % p for p in propostas] + [""]
    if falhas:
        rel += ["## Não consegui ler", ""] + ["- %s" % f for f in falhas] + [""]
    rel += ["## Detalhe por banco"] + linhas + [""]
    (destino / "precarios.md").write_text("\n".join(rel) + "\n", encoding="utf-8")

    patch_path = destino / "alteracoes.json"
    if taxas_patch:
        patch = {"_nota": "Gerado por scripts/verificar_precarios.py a %s. Só taxas de produtos existentes, cada uma com guarda no valor antigo. Rever antes de aplicar." % hoje,
                 "taxas": [{k: v for k, v in t.items() if not k.startswith("_")} for t in taxas_patch]}
        if not patch_path.exists():
            patch_path.write_text(json.dumps(patch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            print("já existe %s, não o substituí. O patch novo está em alteracoes-precarios.json" % patch_path)
            (destino / "alteracoes-precarios.json").write_text(json.dumps(patch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n".join(rel[:40]))
    print("\nrelatório: %s" % (destino / "precarios.md").relative_to(ROOT))
    print("%d taxas mudaram, %d propostas, %d falhas" % (len(taxas_patch), len(propostas), len(falhas)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
