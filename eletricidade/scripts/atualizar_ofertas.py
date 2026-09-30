#!/usr/bin/env python3
"""Gera eletricidade/data/ofertas.json a partir do ficheiro oficial de ofertas
comerciais da ERSE (o mesmo que alimenta o simulador de precos da ERSE).

Fonte: https://simuladorprecos.erse.pt/ -> "Ofertas comerciais (CSV)".
O caminho do zip muda a cada atualizacao e e lido de /config/Settings.json.
So usa a biblioteca padrao do Python.
"""
import csv, io, json, os, re, sys, urllib.parse, urllib.request, zipfile
from datetime import date, datetime

BASE = "https://simuladorprecos.erse.pt"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "ofertas.json")
POTS = ["1,15", "2,3", "3,45", "4,6", "5,75", "6,9", "10,35", "13,8", "17,25", "20,7"]
UA = {"User-Agent": "Mozilla/5.0 (compatible; LF-eletricidade/1.0; +https://www.literaciafinanceira.pt)"}


def get(url):
    req = urllib.request.Request(urllib.parse.quote(url, safe=":/?=&%"), headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def num(s):
    if s is None or str(s).strip() == "":
        return 0.0
    try:
        return float(str(s).replace(",", "."))
    except ValueError:
        return 0.0


def r5(s):
    n = num(s)
    return round(n, 5) if n else 0


def ler(zf, nome):
    alvo = [n for n in zf.namelist() if n.replace("\\", "/").split("/")[-1] == nome][0]
    txt = zf.read(alvo).decode("utf-8-sig", errors="replace")
    return list(csv.DictReader(io.StringIO(txt), delimiter=";", quoting=csv.QUOTE_NONE))


def main():
    settings = json.loads(get(BASE + "/config/Settings.json").decode("utf-8-sig"))
    caminho = settings["csvPath"]
    zf = zipfile.ZipFile(io.BytesIO(get(caminho)))
    cond = ler(zf, "CondComerciais.csv")
    precos = ler(zf, "Precos_ELEGN.csv")

    m = re.search(r"/(\d{4})(\d{2})(\d{2}) ", urllib.parse.unquote(caminho))
    atualizado = f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else date.today().isoformat()
    ref = datetime.strptime(atualizado, "%Y-%m-%d").date()

    por_cod = {}
    for p in precos:
        por_cod.setdefault(p["COD_Proposta"], {})[(p["Pot_Cont"], p["Contagem"])] = p

    flags = ["FiltroFidelização", "FiltroRenovavel_ELE", "FiltroRestrições", "FiltroPrecosIndex_ELE",
             "FiltroServicosAdic", "FiltroTarifaSocial", "FiltroReembolsos", "FiltroNovosClientes"]
    ofertas = []
    for o in cond:
        if o.get("Fornecimento") != "ELE" or o.get("Segmento") not in ("Dom", "Tod"):
            continue
        fim = (o.get("Data fim") or "").strip()
        if fim:
            try:
                if datetime.strptime(fim, "%d/%m/%Y").date() < ref:
                    continue
            except ValueError:
                pass
        ps = por_cod.get(o["COD_Proposta"], {})
        s, b = [], []
        for pot in POTS:
            p1, p2 = ps.get((pot, "1")), ps.get((pot, "2"))
            if p1 and num(p1["TF"]) and num(p1["TV|TVFV|TVP"]):
                s.append([r5(p1["TF"]), r5(p1["TV|TVFV|TVP"])])
            else:
                s.append(0)
            if p2 and num(p2["TF"]) and num(p2["TV|TVFV|TVP"]) and num(p2["TVV|TVC"]):
                b.append([r5(p2["TF"]), r5(p2["TV|TVFV|TVP"]), r5(p2["TVV|TVC"])])
            else:
                b.append(0)
        if not any(s) and not any(b):
            continue
        x = {
            "id": o["COD_Proposta"], "c": o["COM"], "n": o["NomeProposta"].strip(),
            "f": "".join("1" if o.get(k) == "S" else "0" for k in flags),
            "pg": o.get("FiltroPagamento", ""), "ft": o.get("Filtrofaturacao", ""),
            "u": (o.get("LinkOfertaCom") or o.get("LinkCOM") or "").strip(),
        }
        if (o.get("TxTModalidade") or "").strip():
            x["m"] = o["TxTModalidade"].strip()
        if (o.get("DuracaoContrato") or "").strip().isdigit():
            x["du"] = int(o["DuracaoContrato"])
        if fim:
            x["fim"] = fim
        cs = num(o.get("CustoServicos_c/IVA (€/ano)"))
        if cs:
            x["cs"] = cs
        R = [num(o.get("ReembFixo (€/ano)")), num(o.get("ReembTF_ELE (%)")), num(o.get("ReembTW_ELE (%)")), num(o.get("ReembW_ELE (€/kWh)"))]
        if any(R):
            x["r"] = R
        D = [num(o.get("DescontNovoCliente_c/IVA (€/ano)")), num(o.get("Desc. TF_ELE (%) - Novo Cliente")),
             num(o.get("Desc. TW_ELE (%) - Novo Cliente")), num(o.get("Desc. W_ELE (€/kWh) - Novo Cliente"))]
        if any(D):
            x["d"] = D
        tr = (o.get("TxTRestricoesAdic") or "").strip()
        if tr and tr != "-":
            x["tr"] = tr[:220]
        ts = (o.get("TxTServicoAdic") or "").strip()
        if ts and ts != "-":
            x["ts"] = ts[:160]
        # Formato compacto: s = [termos fixos por potencia, preco kWh]; b = [termos fixos (1 = os de s), fora de vazio, vazio].
        def col(rows, j):
            vals = [r[j] for r in rows if r]
            return vals[0] if len(set(vals)) == 1 else [(r[j] if r else 0) for r in rows]
        if any(s):
            x["s"] = [[(r[0] if r else 0) for r in s], col(s, 1)]
        if any(b):
            tf = [(r[0] if r else 0) for r in b]
            x["b"] = [1 if any(s) and tf == x["s"][0] else tf, col(b, 1), col(b, 2)]
        ofertas.append(x)

    if len(ofertas) < 50:
        sys.exit(f"Apenas {len(ofertas)} ofertas: formato da ERSE pode ter mudado. Nada foi escrito.")
    dados = {
        "v": 2, "fonte": "ERSE - Ofertas comerciais (CSV)", "ficheiro": caminho, "atualizado": atualizado,
        "pots": [float(p.replace(",", ".")) for p in POTS], "ofertas": ofertas,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{len(ofertas)} ofertas, ficheiro ERSE de {atualizado}")


if __name__ == "__main__":
    main()
