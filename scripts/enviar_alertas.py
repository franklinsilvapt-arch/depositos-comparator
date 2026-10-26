#!/usr/bin/env python3
"""Envia os alertas de depósitos a prazo do Literacia Financeira pelo Mailchimp.

Corre depois de cada verificação aprovada (quando data/depositos.json muda). Para cada contacto do grupo
"Alertas: depósitos a prazo" lê o critério (campos DP_PRAZO, DP_TAXA e DP_MONT), procura o melhor depósito
que o cumpre e, se for diferente do último avisado (DP_ULTIMO), grava o resultado em DP_RES e marca o contacto
com a etiqueta "alerta-dp-envio". No fim envia uma campanha só para essa etiqueta e retira-a.

Variáveis de ambiente (secrets do GitHub):
  MAILCHIMP_API_KEY   chave da API (termina em -usNN, que é o servidor)
  MAILCHIMP_LIST_ID   id da audiência
  MAILCHIMP_FROM      email de envio verificado no Mailchimp (ex.: geral@literaciafinanceira.pt)
O grupo "Alertas" e a opção "Depósitos a prazo" são encontrados pelo nome.
Uso: python3 scripts/enviar_alertas.py [--simular]   (--simular mostra o que seria enviado, sem mexer em nada)
"""
import base64, json, os, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG = "alerta-dp-envio"
COMPARADOR = "https://www.literaciafinanceira.pt/comparador-depositos-a-prazo"
CAMPOS = [  # campos do contacto que o script precisa; são criados se não existirem
    ("DP_PRAZO", "Prazo do alerta (meses)", "text"),
    ("DP_TAXA", "TANB mínima do alerta", "text"),
    ("DP_MONT", "Montante do alerta", "text"),
    ("DP_ULTIMO", "Último depósito avisado", "text"),
    ("DP_RES", "Resultado do alerta", "text"),
]


def pct(v):
    return f"{v:.2f}".replace(".", ",") + "%"


def eur(v):
    return f"{v:,.0f}".replace(",", ".") + "€"


class MC:
    def __init__(self, key):
        self.dc = key.rsplit("-", 1)[1]
        self.auth = "Basic " + base64.b64encode(f"lf:{key}".encode()).decode()

    def req(self, method, path, body=None):
        url = f"https://{self.dc}.api.mailchimp.com/3.0{path}"
        data = json.dumps(body).encode() if body is not None else None
        r = urllib.request.Request(url, data=data, method=method, headers={"Authorization": self.auth, "Content-Type": "application/json"})
        with urllib.request.urlopen(r, timeout=60) as resp:
            txt = resp.read().decode()
            return json.loads(txt) if txt else {}


def melhor(depositos, prazo, taxa, mont):
    ok = []
    for x in depositos:
        if x.get("a_confirmar") or x.get("idade_max"):
            continue
        p = x["prazos"].get(str(prazo))
        if not p:
            continue
        mn = p.get("min", x.get("min") or 0)
        mx = p.get("max", x.get("max"))
        if p["tanb"] >= taxa and mont >= mn and (mx is None or mont <= mx):
            ok.append((p["tanb"], x))
    ok.sort(key=lambda a: -a[0])
    return ok


def main():
    simular = "--simular" in sys.argv
    d = json.loads((ROOT / "data/depositos.json").read_text(encoding="utf-8"))
    deps = d["depositos"]
    key = os.environ.get("MAILCHIMP_API_KEY")
    lst = os.environ.get("MAILCHIMP_LIST_ID")
    if not (key and lst):
        print("Faltam MAILCHIMP_API_KEY ou MAILCHIMP_LIST_ID: nada a fazer.")
        return
    mc = MC(key)
    cats = mc.req("GET", f"/lists/{lst}/interest-categories?count=60")["categories"]
    cat = next((c for c in cats if c["title"].strip().lower() == "alertas"), None)
    if not cat:
        print('Não encontrei o grupo "Alertas" na audiência.'); return
    ints = mc.req("GET", f"/lists/{lst}/interest-categories/{cat['id']}/interests?count=60")["interests"]
    it = next((i for i in ints if i["name"].strip().lower() == "depósitos a prazo"), None)
    if not it:
        print('Não encontrei a opção "Depósitos a prazo" no grupo "Alertas".'); return
    categoria, interest = cat["id"], it["id"]

    # Retira a etiqueta da campanha anterior (não se retira logo a seguir ao envio, que é assíncrono).
    seg = next((s for s in mc.req("GET", f"/lists/{lst}/segments?type=static&count=1000")["segments"] if s["name"] == TAG), None)
    if seg and not simular:
        antigos = mc.req("GET", f"/lists/{lst}/segments/{seg['id']}/members?count=1000&fields=members.id")["members"]
        for m in antigos:
            mc.req("POST", f"/lists/{lst}/members/{m['id']}/tags", {"tags": [{"name": TAG, "status": "inactive"}]})

    existentes = {f["tag"] for f in mc.req("GET", f"/lists/{lst}/merge-fields?count=100")["merge_fields"]}
    for tag, nome, tipo in CAMPOS:
        if tag not in existentes and not simular:
            mc.req("POST", f"/lists/{lst}/merge-fields", {"tag": tag, "name": nome, "type": tipo, "public": tag in ("DP_PRAZO", "DP_TAXA", "DP_MONT")})

    membros, off = [], 0
    while True:
        r = mc.req("GET", f"/lists/{lst}/members?status=subscribed&count=500&offset={off}&interest_category_id={categoria}&interest_ids={interest}&interest_match=any&fields=members.id,members.email_address,members.merge_fields,total_items")
        membros += r.get("members", [])
        off += 500
        if off >= r.get("total_items", 0):
            break

    marcados = []
    for m in membros:
        f = m.get("merge_fields", {})
        try:
            prazo = int(f.get("DP_PRAZO") or 0)
            taxa = float(str(f.get("DP_TAXA") or "0").replace(",", "."))
            mont = float(str(f.get("DP_MONT") or "0").replace(".", "").replace(",", "."))
        except ValueError:
            continue
        if not prazo or not taxa or not mont:
            continue
        lista = melhor(deps, prazo, taxa, mont)
        if not lista:
            continue
        t, x = lista[0]
        assinatura = f"{x['id']}@{t}"
        if f.get("DP_ULTIMO") == assinatura:
            continue  # o mesmo depósito à mesma taxa já foi avisado
        extra = f" e mais {len(lista) - 1}" if len(lista) > 1 else ""
        res = f"{x['banco']}, {x['produto']}: {pct(t)} a {prazo} meses{extra}"
        marcados.append((m, assinatura, res))
        print(("[simulação] " if simular else "") + f"{m['email_address']}: {res}")
        if not simular:
            mc.req("PATCH", f"/lists/{lst}/members/{m['id']}", {"merge_fields": {"DP_RES": res[:255], "DP_ULTIMO": assinatura}})
            mc.req("POST", f"/lists/{lst}/members/{m['id']}/tags", {"tags": [{"name": TAG, "status": "active"}]})

    print(f"{len(membros)} contactos com alerta, {len(marcados)} a avisar")
    if simular or not marcados:
        return

    seg = next((s for s in mc.req("GET", f"/lists/{lst}/segments?type=static&count=1000")["segments"] if s["name"] == TAG), None)
    if not seg:
        seg = mc.req("POST", f"/lists/{lst}/segments", {"name": TAG, "static_segment": []})
    data = d["meta"]["data_verificacao"]
    camp = mc.req("POST", "/campaigns", {
        "type": "regular",
        "recipients": {"list_id": lst, "segment_opts": {"saved_segment_id": seg["id"]}},
        "settings": {"subject_line": "Há um depósito a prazo com a taxa que pediste",
                     "preview_text": "*|DP_RES|*",
                     "title": f"Alerta depósitos {data}",
                     "from_name": "Literacia Financeira",
                     "reply_to": os.environ.get("MAILCHIMP_FROM", "geral@literaciafinanceira.pt")},
    })
    corpo = (
        '<div style="font-family:Inter,Arial,sans-serif;font-size:16px;line-height:1.5;color:#202432;max-width:560px">'
        "<p>Olá,</p>"
        "<p>Na verificação de " + data.split("-")[2] + "/" + data.split("-")[1] + "/" + data.split("-")[0] +
        " encontrámos um depósito a prazo que cumpre o teu alerta (*|DP_PRAZO|* meses, TANB de pelo menos *|DP_TAXA|*% para *|DP_MONT|*€):</p>"
        '<p style="font-size:18px"><b>*|DP_RES|*</b></p>'
        f'<p><a href="{COMPARADOR}" style="color:#c72307">Vê todos os depósitos no comparador</a> e confirma as condições no banco antes de subscrever.</p>'
        "<p>Obrigado,<br>Literacia Financeira</p>"
        '<p style="font-size:12px;color:#697386">Recebes este email porque criaste um alerta de depósitos a prazo no Literacia Financeira. '
        '<a href="*|UPDATE_PROFILE|*">Mudar o critério</a> ou <a href="*|UNSUB|*">cancelar</a>. Esta informação não é aconselhamento financeiro.</p>'
        "</div>"
    )
    mc.req("PUT", f"/campaigns/{camp['id']}/content", {"html": corpo})
    mc.req("POST", f"/campaigns/{camp['id']}/actions/send")
    print("campanha enviada:", camp["id"])


if __name__ == "__main__":
    main()
