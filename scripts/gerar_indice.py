#!/usr/bin/env python3
"""Gera data/indice.json (Índice de depósitos a prazo do Literacia Financeira) a partir das cópias
datadas em data/historico/AAAA-MM-DD.json. Cada verificação aprovada (dias 1 e 16) guarda uma cópia
de data/depositos.json em data/historico/ com a data de meta.data_verificacao e corre este script.

Regras do índice:
- Universo: depósitos acessíveis a quem aplica 10.000€ (mínimo <= 10.000€ e máximo >= 10.000€, também
  no prazo), sem limite de idade e sem nada marcado "a_confirmar".
- Campanhas: depósitos só para novos clientes ou para dinheiro novo (campo "novos"). Os restantes são
  "sem condições".
- Mediana em vez de média, para uma campanha alta não puxar o valor.
- Evolução: índice encadeado a 12 meses. Parte da média da primeira verificação e soma, em cada data, a
  variação média (em pontos) dos depósitos presentes nas duas verificações. Assim a série mede mudanças
  de taxa e não a entrada ou saída de depósitos do comparador.
"""
import json, statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HIST = ROOT / "data/historico"
MONTANTE = 10000
PRAZOS = ["3", "6", "12", "24"]

def carregar():
    snaps = []
    for f in sorted(HIST.glob("????-??-??.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        snaps.append((f.stem, d))
    return snaps

def elegivel(x):
    if x.get("a_confirmar") or x.get("idade_max"):
        return False
    mn = x.get("min") or 0
    mx = x.get("max")
    return mn <= MONTANTE and (mx is None or mx >= MONTANTE)

def taxa(x, p):
    o = x["prazos"].get(p)
    if not o or (o.get("min") or 0) > MONTANTE:
        return None
    if o.get("max") is not None and o["max"] < MONTANTE:
        return None
    return o["tanb"]

def resumo(x, t):
    r = {"tanb": t, "banco": x["banco"], "produto": x["produto"], "id": x["id"]}
    if x.get("novos"):
        r["novos"] = x["novos"]
    if x.get("irs_retido") is False:
        r["sem_retencao"] = True
    return r

def melhor(lst):
    return resumo(*max(lst, key=lambda a: (a[1], -len(a[0]["produto"])))) if lst else None

def mediana(vals):
    return round(st.median(vals), 3) if vals else None

def estado(d):
    deps = [x for x in d["depositos"] if elegivel(x)]
    out = {"universo": {"depositos": len(deps), "bancos": len({x["banco"] for x in deps})},
           "comparador": {"depositos": len(d["depositos"]), "bancos": len({x["banco"] for x in d["depositos"]})},
           "prazos": {}}
    for p in PRAZOS:
        todos = [(x, taxa(x, p)) for x in deps if taxa(x, p) is not None]
        camp = [a for a in todos if a[0].get("novos")]
        sem = [a for a in todos if not a[0].get("novos")]
        out["prazos"][p] = {
            "n": len(todos), "n_campanhas": len(camp), "n_sem_condicoes": len(sem),
            "melhor": melhor(todos), "melhor_sem_condicoes": melhor(sem),
            "mediana": mediana([t for _, t in todos]),
            "mediana_campanhas": mediana([t for _, t in camp]) if len(camp) >= 3 else None,
            "mediana_sem_condicoes": mediana([t for _, t in sem]) if len(sem) >= 3 else None,
        }
    return out

def serie_12m(snaps):
    pts, nivel = [], None
    for i, (dt, d) in enumerate(snaps):
        cur = {x["id"]: taxa(x, "12") for x in d["depositos"] if elegivel(x) and taxa(x, "12") is not None}
        if i == 0:
            nivel = st.mean(cur.values()); n = len(cur)
        else:
            prev = prev_map
            pares = [cur[k] - prev[k] for k in cur if k in prev]
            nivel += st.mean(pares) if pares else 0; n = len(pares)
        pts.append({"data": dt, "taxa": round(nivel, 3), "depositos": n})
        prev_map = cur
    return pts

def alteracoes(a, b):
    A = {x["id"]: x for x in a["depositos"]}
    B = {x["id"]: x for x in b["depositos"]}
    sub, desc = [], []
    for i, x in B.items():
        if i not in A:
            continue
        for p, o in x["prazos"].items():
            v = A[i]["prazos"].get(p)
            if v and v["tanb"] != o["tanb"]:
                e = {"banco": x["banco"], "produto": x["produto"], "prazo": int(p), "antes": v["tanb"], "depois": o["tanb"]}
                (sub if o["tanb"] > v["tanb"] else desc).append(e)
    sub.sort(key=lambda e: e["antes"] - e["depois"])
    desc.sort(key=lambda e: e["depois"] - e["antes"])
    return {"subidas": sub, "descidas": desc,
            "entraram": [B[i]["banco"] + ", " + B[i]["produto"] for i in B if i not in A],
            "sairam": [A[i]["banco"] + ", " + A[i]["produto"] for i in A if i not in B]}

def main():
    snaps = carregar()
    datas = [s[0] for s in snaps]
    atual = snaps[-1][1]
    out = {"atualizado": datas[-1], "verificacoes": datas, "montante": MONTANTE, "retencao_irs": 0.28}
    out.update(estado(atual))
    out["serie_12m"] = serie_12m(snaps)
    if len(snaps) > 1:
        out["alteracoes"] = dict(desde=datas[-2], ate=datas[-1], **alteracoes(snaps[-2][1], atual))
    # Edição mensal: a primeira verificação de cada mês fica arquivada com os números desse dia.
    edicoes, vistos = [], set()
    for dt, d in snaps:
        mes = dt[:7]
        if mes in vistos:
            continue
        vistos.add(mes)
        e = estado(d)["prazos"]["12"]
        edicoes.append({"mes": mes, "data": dt, "mediana_12m": e["mediana"],
                        "melhor_12m_sem_condicoes": e["melhor_sem_condicoes"]})
    out["edicoes"] = edicoes
    ref = ROOT / "data/referencias.json"
    if ref.exists():
        out["referencias"] = json.loads(ref.read_text(encoding="utf-8"))["bdp_novos_depositos"]
    (ROOT / "data/indice.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("indice.json:", datas[-1], out["universo"], [(p, out["prazos"][p]["mediana"]) for p in PRAZOS])

if __name__ == "__main__":
    main()
