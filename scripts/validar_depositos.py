#!/usr/bin/env python3
"""Valida data/depositos.json. Corre no CI a cada alteração e antes de instalar
dados novos. Sai com código 1 e lista os problemas se houver algum.

Regras verificadas (as do verificacao/TAREFA.md):
  - JSON válido e com a estrutura esperada
  - campos obrigatórios presentes, sem campos desconhecidos
  - TANB >= 1,00% (meta.regra_inclusao)
  - prazos só em 3, 6, 12 ou 24 meses
  - ids únicos, min/max coerentes, cada entrada com pelo menos uma nota
  - valores fechados de canal, mobilizacao e novos
  - data_verificacao no formato AAAA-MM-DD e não no futuro
"""
import json, re, sys, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALVO = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "data/depositos.json")

OBRIG = {"a_confirmar","banco","canal","custo_conta","id","irs_retido","juros","max",
         "min","mobilizacao","notas","novos","pais","prazos","produto","url","url_fin"}
OPC = {"idade_max","mobil_nota"}
CANAL = {"Balcão e digital","Digital","Balcão"}
MOBIL = {"parcial","total","nao"}
NOVOS = {"clientes","montantes",None}
GRELHA = {"3","6","12","24"}
TANB_MIN = 1.0

erros, avisos = [], []
def erro(i, m): erros.append("%-28s %s" % (i, m))
def aviso(i, m): avisos.append("%-28s %s" % (i, m))

try:
    d = json.loads(Path(ALVO).read_text(encoding="utf-8"))
except Exception as e:
    print("JSON inválido:", e); sys.exit(1)

if "meta" not in d or "depositos" not in d:
    print("Faltam as chaves de topo 'meta' e/ou 'depositos'"); sys.exit(1)

dv = d["meta"].get("data_verificacao", "")
if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", dv or ""):
    erro("meta", "data_verificacao não está em AAAA-MM-DD: %r" % dv)
else:
    try:
        if dt.date.fromisoformat(dv) > dt.date.today():
            erro("meta", "data_verificacao está no futuro: %s" % dv)
    except ValueError:
        erro("meta", "data_verificacao não é uma data real: %s" % dv)

vistos = {}
for e in d["depositos"]:
    i = e.get("id", "<sem id>")
    if i in vistos: erro(i, "id duplicado")
    vistos[i] = e
    faltam = OBRIG - set(e)
    if faltam: erro(i, "faltam campos: %s" % ", ".join(sorted(faltam)))
    extra = set(e) - OBRIG - OPC
    if extra: erro(i, "campos desconhecidos: %s" % ", ".join(sorted(extra)))
    if e.get("canal") not in CANAL: erro(i, "canal inválido: %r" % e.get("canal"))
    if e.get("mobilizacao") not in MOBIL: erro(i, "mobilizacao inválida: %r" % e.get("mobilizacao"))
    if e.get("novos") not in NOVOS: erro(i, "novos inválido: %r" % e.get("novos"))
    if not e.get("notas"): erro(i, "sem notas")
    if not isinstance(e.get("prazos"), dict) or not e["prazos"]:
        erro(i, "sem prazos"); continue
    for p, o in e["prazos"].items():
        if p not in GRELHA: erro(i, "prazo fora da grelha 3/6/12/24: %r" % p)
        if not isinstance(o, dict) or "tanb" not in o:
            erro(i, "prazo %s sem tanb" % p); continue
        if set(o) - {"tanb","min","max"}: erro(i, "prazo %s com chaves estranhas" % p)
        t = o["tanb"]
        if not isinstance(t, (int, float)): erro(i, "prazo %s: tanb não numérico" % p)
        elif t < TANB_MIN: erro(i, "prazo %s: TANB %s abaixo de %s" % (p, t, TANB_MIN))
        elif t > 10: aviso(i, "prazo %s: TANB %s é invulgarmente alta, confirma" % (p, t))
    mn, mx = e.get("min"), e.get("max")
    if mn is not None and mx is not None and mx < mn:
        erro(i, "max (%s) menor que min (%s)" % (mx, mn))
    uf = e.get("url_fin")
    if uf and not str(uf).startswith("http"):
        aviso(i, "url_fin é nome de documento, não link: o verificador automático falha nesta linha")
    if not str(e.get("url", "")).startswith("http"):
        erro(i, "url não é um link: %r" % e.get("url"))

print("%s: %d depósitos, verificado em %s" % (ALVO, len(d["depositos"]), dv))
if avisos:
    print("\nAVISOS (%d), não bloqueiam:" % len(avisos))
    for a in avisos: print("  ", a)
if erros:
    print("\nERROS (%d):" % len(erros))
    for x in erros: print("  ", x)
    sys.exit(1)
print("\nOK, sem erros.")
