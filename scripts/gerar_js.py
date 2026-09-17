#!/usr/bin/env python3
"""Gera comparador-depositos.js a partir de data/depositos.json (bloco de dados) e de
scripts/comparador-template.js (lógica). Corre automaticamente no workflow depois de
qualquer alteração ao JSON: só se edita o JSON."""
import json, re, datetime as dt
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
d = json.loads((ROOT / "data/depositos.json").read_text(encoding="utf-8"))
L = "https://cdn.prod.website-files.com/67922c46c9da6bf5d9bfdf09/"
LOGOS = d.get("logos", {})
INI = {'Banco BiG':'BiG','ActivoBank':'AB','Banco Português de Gestão':'BPG','Banco Best':'Bt','Banco Carregosa':'BC','Haitong Bank':'HB','BAI Europa':'BAI','Banco Invest':'In','Klarna':'K','Banco Finantia':'BF','Atlântico Europa':'At','Openbank':'Ob','Bankinter':'Bk','BNI Europa':'BNI','Banco CTT':'CTT','Bison Bank':'Bi','BPI':'BPI','Caixa Geral de Depósitos':'CGD'}
MESES = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]
def data_pt(iso):
    y, m, dd = iso.split("-"); return f"{int(dd)} de {MESES[int(m)-1]} de {y}"
parts = []
for x in d["depositos"]:
    pr = {}
    for m, o in x["prazos"].items():
        if "min" in o or "max" in o:
            q = {"tan": o["tanb"]}
            if "min" in o: q["min"] = o["min"]
            if "max" in o: q["max"] = o["max"]
            pr[int(m)] = q
        else:
            pr[int(m)] = o["tanb"]
    o = {"id": x["id"], "banco": x["banco"], "ini": INI.get(x["banco"], x["banco"][:2]), "produto": x["produto"], "prazos": pr, "min": x["min"]}
    if x.get("max") is not None: o["max"] = x["max"]
    if x.get("novos"): o["novos"] = x["novos"]
    if x["mobilizacao"] != "nao": o["mobil"] = x["mobilizacao"]
    if x.get("canal") == "Digital": o["canal"] = "Digital"
    if x.get("custo_conta"): o["custoConta"] = x["custo_conta"]
    if not x.get("irs_retido", True): o["irsRetido"] = False
    if x.get("pais", "PT") != "PT": o["pais"] = x["pais"]
    o["url"] = x["url"]; o["notas"] = x["notas"]
    s = json.dumps(o, ensure_ascii=False, separators=(",", ":"))
    if x["banco"] in LOGOS:
        lg = LOGOS[x["banco"]]
        s = s[:-1] + (',"logo":"' + lg + '"}' if lg.startswith("http") else ',"logo":L+"' + lg + '"}')
    parts.append("i(" + s + ")")
arr = "n=[" + ",".join(parts) + "]"
tpl = (ROOT / "scripts/comparador-template.js").read_text(encoding="utf-8")
out = tpl.replace("/*__DADOS__*/", arr).replace("/*__DATA__*/", data_pt(d["meta"]["data_verificacao"]))
(ROOT / "comparador-depositos.js").write_text("/* Gerado por scripts/gerar_js.py a partir de data/depositos.json. Não editar à mão. */\n" + out + "\n", encoding="utf-8")
print("comparador-depositos.js gerado:", len(out), "caracteres,", len(d["depositos"]), "depósitos")
