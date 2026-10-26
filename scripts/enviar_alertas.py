#!/usr/bin/env python3
"""Envia os alertas por email do Literacia Financeira pelo Mailchimp (público "Alertas Literacia Financeira").

Quatro tipos de alerta, cada um com os seus campos no contacto:
  dp  depósitos a prazo   DP_PRAZO, DP_TAXA, DP_MONT            -> depósito com TANB >= taxa no prazo e montante
  el  eletricidade        EL_PERFIL, EL_MAX                     -> oferta mais barata do tipo de casa abaixo de EL_MAX €/ano
  eu  Euribor             EU_PRAZO, EU_DIR, EU_TAXA             -> Euribor a N meses abaixo/acima de EU_TAXA %
  co  corretoras          CO_ID                                 -> a corretora mudou custos ou condições no comparador
Cada tipo guarda o que já avisou em *_ULTIMO, para não repetir o mesmo email, e o texto do aviso em *_RES.

Por cada tipo com contactos a avisar: grava *_RES, marca-os com a etiqueta "alerta-XX-envio" e envia uma campanha
só para essa etiqueta. As etiquetas da execução anterior são retiradas no início (o envio é assíncrono).

Corre todos os dias e depois de cada verificação dos depósitos (workflow enviar-alertas.yml).
Variáveis de ambiente (secrets do GitHub): MAILCHIMP_API_KEY, MAILCHIMP_LIST_ID, MAILCHIMP_FROM (opcional).
Uso: python3 scripts/enviar_alertas.py [--simular]   (--simular mostra o que seria enviado, sem mexer em nada)
"""
import base64, hashlib, json, os, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIMULAR = "--simular" in sys.argv
SITE = "https://www.literaciafinanceira.pt"
URL_EL = "https://franklinsilvapt-arch.github.io/comparador-eletricidade/comparador-eletricidade/data/indice.json"
URL_EU = "https://raw.githubusercontent.com/franklinsilvapt-arch/euribor-hoje/main/euribor-data.json"
URL_CO = "https://franklinsilvapt-arch.github.io/corretoras-comparator/data/corretoras.json"
ESTADO_CO = ROOT / "data/alertas/corretoras-anterior.json"

CAMPOS = [  # (tag, nome, público no formulário de preferências)
    ("DP_PRAZO", "Depósitos: prazo (meses)", True), ("DP_TAXA", "Depósitos: TANB mínima", True),
    ("DP_MONT", "Depósitos: montante", True), ("DP_ULTIMO", "Depósitos: último avisado", False), ("DP_RES", "Depósitos: resultado", False),
    ("EL_PERFIL", "Eletricidade: tipo de casa (p1 ou p2)", True), ("EL_MAX", "Eletricidade: custo anual máximo", True),
    ("EL_ULTIMO", "Eletricidade: último avisado", False), ("EL_RES", "Eletricidade: resultado", False),
    ("EU_PRAZO", "Euribor: prazo (meses)", True), ("EU_DIR", "Euribor: abaixo ou acima", True), ("EU_TAXA", "Euribor: valor", True),
    ("EU_ULTIMO", "Euribor: último estado", False), ("EU_RES", "Euribor: resultado", False),
    ("CO_ID", "Corretoras: corretora", True), ("CO_ULTIMO", "Corretoras: último avisado", False), ("CO_RES", "Corretoras: resultado", False),
]
ROTULOS_CO = {
    "etfFee": "ETFs europeus", "pt": "Ações portuguesas", "usFee": "Ações dos EUA", "fx": "Câmbio",
    "venue": "Onde são executadas as ordens", "custodyTxt": "Custódia", "inact": "Inatividade",
    "transfer": "Transferir títulos para outra corretora", "interest": "Juros sobre o dinheiro parado",
    "entity": "Entidade que serve clientes em Portugal", "regulator": "Regulador", "presence": "Presença em Portugal",
    "protInv": "Proteção dos investimentos", "protCash": "Proteção do dinheiro", "tax": "Retenção de IRS",
    "annex": "Onde declaras no IRS", "ptStocks": "Ações da Euronext Lisboa", "fractions": "Frações de ações e ETFs",
    "plans": "Planos de investimento automático", "bonds": "Obrigações", "options": "Opções", "iban": "IBAN português",
}
PERFIS = {"p1": "casal sem filhos", "p2": "casal com 2 filhos"}


def pct(v):
    return f"{v:.2f}".replace(".", ",") + "%"


def eur(v):
    return f"{v:,.0f}".replace(",", ".") + "€"


def num(x):
    try:
        return float(str(x or "").replace(",", "."))
    except ValueError:
        return 0.0


def get_json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "lf-alertas"}), timeout=60) as r:
        return json.loads(r.read().decode())


class MC:
    def __init__(self, key, lst):
        self.dc = key.rsplit("-", 1)[1]
        self.auth = "Basic " + base64.b64encode(f"lf:{key}".encode()).decode()
        self.lst = lst

    def req(self, method, path, body=None):
        url = f"https://{self.dc}.api.mailchimp.com/3.0{path}"
        data = json.dumps(body).encode() if body is not None else None
        r = urllib.request.Request(url, data=data, method=method, headers={"Authorization": self.auth, "Content-Type": "application/json"})
        with urllib.request.urlopen(r, timeout=60) as resp:
            txt = resp.read().decode()
            return json.loads(txt) if txt else {}

    def segmento(self, nome):
        segs = self.req("GET", f"/lists/{self.lst}/segments?type=static&count=1000")["segments"]
        return next((s for s in segs if s["name"] == nome), None)

    def etiqueta(self, mid, nome, ativa):
        self.req("POST", f"/lists/{self.lst}/members/{mid}/tags", {"tags": [{"name": nome, "status": "active" if ativa else "inactive"}]})


# ---------- regras de cada tipo: devolvem (avisar, assinatura, resultado) ou None ----------

def regra_dp(f, deps):
    prazo, taxa, mont = int(num(f.get("DP_PRAZO"))), num(f.get("DP_TAXA")), num(str(f.get("DP_MONT") or "").replace(".", ""))
    if not (prazo and taxa and mont):
        return None
    ok = []
    for x in deps["depositos"]:
        if x.get("a_confirmar") or x.get("idade_max"):
            continue
        p = x["prazos"].get(str(prazo))
        if not p:
            continue
        mn, mx = p.get("min", x.get("min") or 0), p.get("max", x.get("max"))
        if p["tanb"] >= taxa and mont >= mn and (mx is None or mont <= mx):
            ok.append((p["tanb"], x))
    if not ok:
        return None
    ok.sort(key=lambda a: -a[0])
    t, x = ok[0]
    extra = f" e mais {len(ok) - 1}" if len(ok) > 1 else ""
    return True, f"{x['id']}@{t}", f"{x['banco']}, {x['produto']}: {pct(t)} a {prazo} meses{extra}"


def regra_el(f, el):
    perfil, mx = f.get("EL_PERFIL"), num(f.get("EL_MAX"))
    p = next((x for x in el["perfis"] if x["id"] == perfil), None)
    if not (p and mx) or p["melhor"]["total"] >= mx:
        return None
    m = p["melhor"]
    return True, f"{m['id']}@{round(m['total'])}", f"{m['comercializador']}, {m['oferta']}: {eur(m['total'])} por ano para um {PERFIS.get(perfil, perfil)}"


def regra_eu(f, eu):
    prazo, d, taxa = int(num(f.get("EU_PRAZO"))), f.get("EU_DIR"), num(f.get("EU_TAXA"))
    if prazo not in (3, 6, 12) or d not in ("abaixo", "acima") or not taxa:
        return None
    u = eu["serie"][-1]
    v = u[f"m{prazo}"]
    dentro = v < taxa if d == "abaixo" else v > taxa
    if not dentro:
        # Volta a armar o alerta quando a Euribor regressa ao outro lado do valor.
        return (False, "fora", "") if str(f.get("EU_ULTIMO", "")).startswith("dentro") else None
    if str(f.get("EU_ULTIMO", "")).startswith("dentro"):
        return None
    return True, f"dentro@{u['d']}", f"Euribor a {prazo} meses em {pct(v)} a {u['d']} ({d} de {pct(taxa)})"


def mudancas_co(atual, anterior):
    """Por corretora: lista dos campos que mudaram desde a última execução."""
    ant = {c["id"]: c for c in (anterior or {}).get("corretoras", [])}
    out = {}
    for c in atual["corretoras"]:
        a = ant.get(c["id"])
        if not a:
            continue
        mud = [k for k in c.get("t", {}) if c["t"].get(k) != a.get("t", {}).get(k)]
        if mud:
            out[c["id"]] = mud
    return out


def regra_co(f, co, mud):
    cid = f.get("CO_ID")
    c = next((x for x in co["corretoras"] if x["id"] == cid), None)
    if not c or cid not in mud:
        return None
    assin = hashlib.sha1(json.dumps(c.get("t", {}), sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]
    if f.get("CO_ULTIMO") == assin:
        return None
    campos = [ROTULOS_CO.get(k, k) for k in mud[cid]]
    lista = ", ".join(campos[:4]) + (f" e mais {len(campos) - 4}" if len(campos) > 4 else "")
    return True, assin, f"{c['name']} mudou: {lista}"


# ---------- emails ----------

def corpo(titulo, intro, destaque, botao, url, nota, motivo):
    return (
        '<div style="background:#f5f6f8;padding:24px 12px;font-family:Inter,Arial,sans-serif;color:#202432">'
        '<div style="max-width:560px;margin:0 auto;background:#ffffff;border-radius:16px;padding:32px 28px">'
        '<p style="margin:0 0 24px;font-size:18px;font-weight:700;color:#c72307">Literacia Financeira</p>'
        f'<h1 style="margin:0 0 12px;font-size:22px;line-height:1.3;font-weight:600">{titulo}</h1>'
        f'<p style="margin:0 0 20px;font-size:16px;line-height:1.5">{intro}</p>'
        f'<div style="background:#fbf1ef;border-radius:12px;padding:16px 18px;margin:0 0 24px;font-size:17px;line-height:1.45;font-weight:600">{destaque}</div>'
        f'<p style="margin:0 0 24px"><a href="{url}" style="display:inline-block;background:#c72307;color:#ffffff;text-decoration:none;font-weight:600;font-size:16px;padding:12px 20px;border-radius:8px">{botao}</a></p>'
        f'<p style="margin:0 0 8px;font-size:14px;line-height:1.5;color:#4b5263">{nota}</p>'
        '<p style="margin:0;font-size:14px;line-height:1.5;color:#4b5263">Obrigado,<br>Literacia Financeira</p>'
        '</div>'
        '<p style="max-width:560px;margin:16px auto 0;font-size:12px;line-height:1.5;color:#697386;text-align:center">'
        f'Recebes este email porque criaste um alerta {motivo} no Literacia Financeira. '
        '<a href="*|UPDATE_PROFILE|*" style="color:#697386">Mudar o critério</a> ou <a href="*|UNSUB|*" style="color:#697386">cancelar o alerta</a>. '
        'Esta informação não é aconselhamento financeiro.<br>*|LIST:ADDRESSLINE|*</p>'
        '</div>'
    )


def emails(data_txt):
    return {
        "dp": dict(
            assunto="Há um depósito a prazo com a taxa que pediste", previa="*|DP_RES|*",
            html=corpo("Encontrámos um depósito que cumpre o teu alerta",
                       f"Na verificação de {data_txt} há um depósito a *|DP_PRAZO|* meses com TANB de pelo menos *|DP_TAXA|*%, a taxa que pediste no teu alerta:",
                       "*|DP_RES|*", "Ver no comparador", f"{SITE}/comparador-depositos-a-prazo",
                       "Confirma as condições no site do banco antes de subscrever.", "de depósitos a prazo")),
        "el": dict(
            assunto="A eletricidade ficou abaixo do valor que pediste", previa="*|EL_RES|*",
            html=corpo("Há uma oferta de eletricidade abaixo do teu limite",
                       "A oferta mais barata para o teu tipo de casa ficou abaixo de *|EL_MAX|*€ por ano, com os preços publicados pela ERSE.",
                       "*|EL_RES|*", "Simular com o meu consumo", f"{SITE}/comparador-eletricidade",
                       "O custo é estimado para um consumidor-tipo. Simula com a tua fatura para ver quanto pagas tu.", "de eletricidade")),
        "eu": dict(
            assunto="A Euribor passou o valor do teu alerta", previa="*|EU_RES|*",
            html=corpo("A Euribor passou o valor que escolheste",
                       "A Euribor a *|EU_PRAZO|* meses passou o valor do teu alerta.",
                       "*|EU_RES|*", "Ver o impacto na prestação", f"{SITE}/simulador-euribor-prestacao",
                       "A prestação só muda na próxima revisão do teu crédito, com a Euribor dessa data.", "da Euribor")),
        "co": dict(
            assunto="A corretora que segues mudou os custos", previa="*|CO_RES|*",
            html=corpo("A corretora que segues mudou",
                       "Na última revisão dos preçários encontrámos mudanças na corretora do teu alerta.",
                       "*|CO_RES|*", "Ver no comparador", f"{SITE}/comparador-de-corretoras",
                       "Confirma sempre o preçário no site da corretora. Investir envolve risco de perda de capital.", "de corretoras")),
    }


def main():
    key, lst = os.environ.get("MAILCHIMP_API_KEY"), os.environ.get("MAILCHIMP_LIST_ID")
    if not (key and lst):
        print("Faltam MAILCHIMP_API_KEY ou MAILCHIMP_LIST_ID: nada a fazer.")
        return
    mc = MC(key, lst)

    # Dados de cada tipo. Uma fonte em baixo não impede os outros alertas.
    deps = json.loads((ROOT / "data/depositos.json").read_text(encoding="utf-8"))
    fontes = {"dp": deps}
    for t, url in (("el", URL_EL), ("eu", URL_EU), ("co", URL_CO)):
        try:
            fontes[t] = get_json(url)
        except Exception as e:  # noqa: BLE001
            print(f"[{t}] sem dados ({e}): este tipo fica para a próxima execução")
    mud = {}
    if "co" in fontes:
        anterior = json.loads(ESTADO_CO.read_text(encoding="utf-8")) if ESTADO_CO.exists() else None
        mud = mudancas_co(fontes["co"], anterior)
        if mud:
            print("[co] mudanças:", mud)
        if not SIMULAR:
            ESTADO_CO.parent.mkdir(parents=True, exist_ok=True)
            ESTADO_CO.write_text(json.dumps(fontes["co"], ensure_ascii=False, indent=1), encoding="utf-8")

    if not SIMULAR:
        # Retira as etiquetas da execução anterior.
        for t in ("dp", "el", "eu", "co"):
            seg = mc.segmento(f"alerta-{t}-envio")
            if seg:
                for m in mc.req("GET", f"/lists/{lst}/segments/{seg['id']}/members?count=1000&fields=members.id")["members"]:
                    mc.etiqueta(m["id"], f"alerta-{t}-envio", False)
        existentes = {f["tag"] for f in mc.req("GET", f"/lists/{lst}/merge-fields?count=100")["merge_fields"]}
        for tag, nome, publico in CAMPOS:
            if tag not in existentes:
                mc.req("POST", f"/lists/{lst}/merge-fields", {"tag": tag, "name": nome, "type": "text", "public": publico})

    membros, off = [], 0
    while True:
        r = mc.req("GET", f"/lists/{lst}/members?status=subscribed&count=500&offset={off}&fields=members.id,members.email_address,members.merge_fields,total_items")
        membros += r.get("members", [])
        off += 500
        if off >= r.get("total_items", 0):
            break

    regras = {"dp": lambda f: regra_dp(f, fontes["dp"]),
              "el": lambda f: regra_el(f, fontes["el"]) if "el" in fontes else None,
              "eu": lambda f: regra_eu(f, fontes["eu"]) if "eu" in fontes else None,
              "co": lambda f: regra_co(f, fontes["co"], mud) if "co" in fontes else None}
    marcados = {t: [] for t in regras}
    for m in membros:
        f = m.get("merge_fields", {})
        for t, regra in regras.items():
            r = regra(f)
            if not r:
                continue
            avisar, assin, res = r
            pre = t.upper()
            if avisar and f.get(f"{pre}_ULTIMO") == assin:
                continue
            print(("[simulação] " if SIMULAR else "") + f"[{t}] {m['email_address']}: {res if avisar else 'volta a armar o alerta'}")
            if SIMULAR:
                continue
            patch = {f"{pre}_ULTIMO": assin}
            if avisar:
                patch[f"{pre}_RES"] = res[:255]
            mc.req("PATCH", f"/lists/{lst}/members/{m['id']}", {"merge_fields": patch})
            if avisar:
                mc.etiqueta(m["id"], f"alerta-{t}-envio", True)
                marcados[t].append(m["id"])

    print(f"{len(membros)} contactos; a avisar: " + ", ".join(f"{t}={len(v)}" for t, v in marcados.items()))
    if SIMULAR:
        return
    d = deps["meta"]["data_verificacao"].split("-")
    textos = emails(f"{d[2]}/{d[1]}/{d[0]}")
    for t, ids in marcados.items():
        if not ids:
            continue
        nome = f"alerta-{t}-envio"
        seg = mc.segmento(nome) or mc.req("POST", f"/lists/{lst}/segments", {"name": nome, "static_segment": []})
        e = textos[t]
        camp = mc.req("POST", "/campaigns", {
            "type": "regular",
            "recipients": {"list_id": lst, "segment_opts": {"saved_segment_id": seg["id"]}},
            "settings": {"subject_line": e["assunto"], "preview_text": e["previa"],
                         "title": f"Alerta {t} {deps['meta']['data_verificacao']}",
                         "from_name": "Literacia Financeira",
                         "reply_to": os.environ.get("MAILCHIMP_FROM", "geral@literaciafinanceira.pt")},
        })
        mc.req("PUT", f"/campaigns/{camp['id']}/content", {"html": e["html"]})
        mc.req("POST", f"/campaigns/{camp['id']}/actions/send")
        print(f"[{t}] campanha enviada: {camp['id']} para {len(ids)} contactos")


if __name__ == "__main__":
    main()
