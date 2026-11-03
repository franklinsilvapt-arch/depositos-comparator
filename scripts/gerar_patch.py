#!/usr/bin/env python3
"""Compara duas versões de depositos.json e escreve o ficheiro de alterações
que transforma a primeira na segunda. Ferramenta de apoio: serve para produzir
o patch a partir de um ficheiro já construído e revisto.

Uso: python3 scripts/gerar_patch.py antigo.json novo.json > alteracoes.json
"""
import json, sys
a = json.load(open(sys.argv[1], encoding="utf-8"))
b = json.load(open(sys.argv[2], encoding="utf-8"))
A = {e["id"]: e for e in a["depositos"]}
B = {e["id"]: e for e in b["depositos"]}
p = {}
if a["meta"].get("data_verificacao") != b["meta"].get("data_verificacao"):
    p["data_verificacao"] = b["meta"]["data_verificacao"]
taxas, campos, nsub, nadd, novos, remover = [], [], [], [], [], []
for i in A:
    if i not in B:
        remover.append({"id": i, "porque": ""}); continue
    for pr, o in A[i]["prazos"].items():
        if pr in B[i]["prazos"] and o["tanb"] != B[i]["prazos"][pr]["tanb"]:
            taxas.append({"id": i, "prazo": pr, "de": o["tanb"], "para": B[i]["prazos"][pr]["tanb"]})
    for k in set(A[i]) | set(B[i]):
        if k in ("prazos", "notas"): continue
        if A[i].get(k) != B[i].get(k):
            campos.append({"id": i, "campo": k, "de": A[i].get(k), "para": B[i].get(k)})
    na, nb = A[i]["notas"], B[i]["notas"]
    for j, n in enumerate(na):
        if j < len(nb) and nb[j] != n:
            nsub.append({"id": i, "antigo": n, "novo": nb[j]})
    for n in nb[len(na):]:
        nadd.append({"id": i, "texto": n})
for i in B:
    if i not in A: novos.append(B[i])
for k, v in (("taxas",taxas),("campos",campos),("notas_sub",nsub),("notas_add",nadd),("novos",novos),("remover",remover)):
    if v: p[k] = v
print(json.dumps(p, ensure_ascii=False, indent=2))
