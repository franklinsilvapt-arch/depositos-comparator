#!/usr/bin/env python3
"""Envia os alertas por email do Literacia Financeira pelo Mailchimp (público "Alertas Literacia Financeira").

Quatro tipos de alerta, cada um com os seus campos no contacto:
  dp  depósitos a prazo   DP_PRAZO, DP_TAXA, DP_MONT            -> depósito com TANB >= taxa no prazo e montante
  el  eletricidade        EL_PERFIL, EL_MAX                     -> (índice) oferta mais barata do tipo de casa abaixo de EL_MAX €/ano
                          EL_POT, EL_KWH, EL_MES                -> (comparador) oferta de preço fixo abaixo de EL_MES €/mês
                                                                   para o consumo simulado pela pessoa
  eu  Euribor             EU_PRAZO, EU_DIR, EU_TAXA             -> Euribor a N meses abaixo/acima de EU_TAXA %
  co  corretoras          CO_ID                                 -> a corretora mudou custos ou condições no comparador
  dm  resumo mensal       DM = "1"                              -> uma vez por mês, as melhores taxas de depósitos e o que
                                                                   mudou no último mês (o mesmo email para todos)
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
URL_EL_OFERTAS = "https://franklinsilvapt-arch.github.io/comparador-eletricidade/comparador-eletricidade/data/ofertas.json"
URL_EU = "https://raw.githubusercontent.com/franklinsilvapt-arch/euribor-hoje/main/euribor-data.json"
URL_CO = "https://franklinsilvapt-arch.github.io/corretoras-comparator/data/corretoras.json"
ESTADO_CO = ROOT / "data/alertas/corretoras-anterior.json"

CAMPOS = [  # (tag, nome, público no formulário de preferências)
    ("DP_PRAZO", "Depósitos: prazo (meses)", True), ("DP_TAXA", "Depósitos: TANB mínima", True),
    ("DP_MONT", "Depósitos: montante", True), ("DP_ULTIMO", "Depósitos: último avisado", False), ("DP_RES", "Depósitos: resultado", False),
    ("EL_PERFIL", "Eletricidade: tipo de casa (p1 ou p2)", True), ("EL_MAX", "Eletricidade: custo anual máximo", True),
    ("EL_POT", "Eletricidade: potência (índice)", False), ("EL_KWH", "Eletricidade: consumo anual (kWh)", False),
    ("EL_MES", "Eletricidade: fatura mensal máxima", True),
    ("EL_ULTIMO", "Eletricidade: último avisado", False), ("EL_RES", "Eletricidade: resultado", False),
    ("EU_PRAZO", "Euribor: prazo (meses)", True), ("EU_DIR", "Euribor: abaixo ou acima", True), ("EU_TAXA", "Euribor: valor", True),
    ("EU_ULTIMO", "Euribor: último estado", False), ("EU_RES", "Euribor: resultado", False),
    ("DM", "Depósitos: resumo mensal (1 = sim)", True), ("DM_ULTIMO", "Depósitos: último resumo enviado (mês)", False),
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
PERFIS = {"p1": "casal sem filhos", "p2": "casal com 2 filhos", "p3": "casal com 4 filhos"}


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


# Custo anual de uma oferta na tarifa simples. Cópia de custo() em comparador-eletricidade/scripts/gerar_indice.py,
# que por sua vez reproduz calcOpcao() do comparador (validada ao cêntimo). Se mudar lá, muda aqui.
DGEG = 0.07


def custo_el(d, o, i, kwh, novo=True):
    P = d.get("params", {})
    arr = o.get("s")
    if not arr:
        return None
    tfs = o["s"][0]
    if not isinstance(tfs, list) or i >= len(tfs) or not tfs[i]:
        return None
    vals = [tfs[i]]
    for a in arr[1:]:
        x = a[i] if isinstance(a, list) else a
        if not x:
            return None
        vals.append(x)
    TAR = P.get("TAR_POT", [0.0573, 0.1145, 0.1718]); IEC = P.get("IEC", 0.001); CAV = P.get("CAV", 2.85)
    KIVA = P.get("KWH_IVA6", 200); CAVMIN = P.get("CAV_MIN_KWH", 400)
    pot = d["pots"][i]
    tar_dia = TAR[i] if i < len(TAR) else 0
    cav_mes = 0 if kwh < CAVMIN else CAV
    lim = KIVA * 365 / 30
    sh6 = min(1, lim / kwh) if pot <= 6.9 and kwh > 0 else 0
    iva_e = sh6 * 1.06 + (1 - sh6) * 1.23
    en = vals[1] * kwh
    tf = vals[0] * 365; tar = tar_dia * 365
    tf_iva = tar * 1.06 + (tf - tar) * 1.23 if pot <= 3.45 else tf * 1.23

    def desc(a):
        return a[0] + a[1] * tf * 1.23 + (a[2] * (en + kwh * IEC) + a[3] * kwh) * iva_e if a else 0
    return en * iva_e + tf_iva + kwh * IEC * 1.23 + cav_mes * 12 * 1.06 + DGEG * 12 * 1.23 + (o.get("cs") or 0) - desc(o.get("r")) - (desc(o.get("d")) if novo else 0)


def melhor_el(ofertas, i, kwh):
    """Oferta de preço fixo mais barata (sem indexadas nem regulado) para a potência i e o consumo anual kwh."""
    melhor = None
    for o in ofertas["ofertas"]:
        if o.get("c") == "TUR" or o.get("f", "0000")[3] == "1":
            continue
        t = custo_el(ofertas, o, i, kwh)
        if t is not None and (melhor is None or t < melhor[0]):
            melhor = (t, o)
    return melhor


# Consumidores-tipo da ERSE usados no índice: potência (kVA) e consumo anual (kWh).
PERFIS_EL = {"p1": (3.45, 1900), "p2": (6.9, 5000), "p3": (13.8, 10900)}


def base_perfil_el(f, ofertas):
    """Quem se inscreveu no índice escolheu um tipo de casa. Passa a ter o mesmo alerta do comparador: guarda a potência,
    o consumo e, como referência, a oferta mais barata de hoje menos 0,50€ por mês. Devolve os campos a gravar ou None."""
    perfil = PERFIS_EL.get(f.get("EL_PERFIL"))
    if not perfil or f.get("EL_KWH") or perfil[0] not in ofertas.get("pots", []):
        return None
    i = ofertas["pots"].index(perfil[0])
    m = melhor_el(ofertas, i, perfil[1])
    if not m:
        return None
    return {"EL_POT": str(i), "EL_KWH": str(perfil[1]), "EL_MES": f"{m[0] / 12 - 0.5:.2f}"}


def regra_el_consumo(f, ofertas):
    """Comparador: oferta de preço fixo (sem indexadas nem regulado) abaixo de EL_MES por mês para o consumo da pessoa."""
    try:
        i, kwh, mes = int(num(f.get("EL_POT"))), num(f.get("EL_KWH")), num(f.get("EL_MES"))
    except ValueError:
        return None
    if not (kwh and mes) or i < 0 or i >= len(ofertas.get("pots", [])):
        return None
    melhor = melhor_el(ofertas, i, kwh)
    if not melhor or melhor[0] / 12 >= mes:
        return None
    t, o = melhor
    nome = NOMES_EL.get(o["c"], o["c"])
    return True, f"{o.get('id')}@{round(t / 12, 1)}", f"{nome}, {o.get('n')}: {f'{t / 12:.2f}'.replace('.', ',')}€ por mês para o teu consumo"


NOMES_EL = {"ALFAENERGIA": "Alfa Energia", "AUDAX": "Audax", "COOP": "Coopérnico", "EDPC": "EDP", "END": "Endesa",
            "ENIPLENITUDE": "Plenitude", "EZUENERGIA": "EZU Energia", "GALP": "Galp", "GOLD": "Goldenergy", "IBD": "Iberdrola",
            "IBELECTRA": "Ibelectra", "JAFPLUS": "JAFplus", "LUZBOA": "Luzboa", "LUZIGAS": "Luzigás", "MUON": "MUON",
            "MEOENERGIA": "MEO Energia", "NABALIAENERGIA": "Nabalia Energia", "NOSSAENERGIA": "Nossa Energia", "OENEO": "Oeneo",
            "PORTULOGOS": "Portulogos", "REPSOL": "Repsol", "YESENERGY": "Yes Energy", "ACCIONA": "Acciona", "ELERGONE": "Elergone",
            "LOGICA": "Logica Energy", "ZUG POWER": "Zug Power", "G9": "G9", "ROCKWATT": "Rockwatt"}


def regra_eu(f, eu):
    prazo, d, taxa = int(num(f.get("EU_PRAZO"))), f.get("EU_DIR"), num(f.get("EU_TAXA"))
    if prazo not in (3, 6, 12) or d not in ("abaixo", "acima", "mudar") or not taxa:
        return None
    u = eu["serie"][-1]
    v = u[f"m{prazo}"]
    if d == "mudar":
        # Avisa quando a Euribor se afasta 0,25 p.p. do último valor avisado (na inscrição, o valor desse dia).
        base = num(str(f.get("EU_ULTIMO", "")).split("@")[0]) or taxa
        if abs(v - base) < 0.25:
            return None
        sentido = "subiu" if v > base else "desceu"
        return True, f"{v}@{u['d']}", f"Euribor a {prazo} meses {sentido} para {pct(v)} a {u['d']} (estava em {pct(base)})"
    dentro = v < taxa if d == "abaixo" else v > taxa
    if not dentro:
        # Volta a armar o alerta quando a Euribor regressa ao outro lado do valor.
        return (False, "fora", "") if str(f.get("EU_ULTIMO", "")).startswith("dentro") else None
    if str(f.get("EU_ULTIMO", "")).startswith("dentro"):
        return None
    return True, f"dentro@{u['d']}", f"Euribor a {prazo} meses em {pct(v)} a {u['d']} ({d} de {pct(taxa)})"


def valor_co(x):
    return (x.get("v") if isinstance(x, dict) else x) or ""


def mudancas_co(atual, anterior):
    """Por corretora: lista dos campos que mudaram desde a última execução."""
    ant = {c["id"]: c for c in (anterior or {}).get("corretoras", [])}
    out = {}
    for c in atual["corretoras"]:
        a = ant.get(c["id"])
        if not a:
            continue
        mud = [(k, valor_co(a.get("t", {}).get(k)), valor_co(c["t"].get(k))) for k in c.get("t", {}) if c["t"].get(k) != a.get("t", {}).get(k)]
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
    partes = []
    for k, antes, depois in mud[cid]:
        rot = ROTULOS_CO.get(k, k)
        # Com valor curto antes e depois, mostra a mudança. Se só mudou a explicação, diz só o que mudou.
        partes.append(f"{rot}: de {antes} para {depois}" if antes and depois and antes != depois and len(antes) + len(depois) < 60 else f"{rot} (condições atualizadas)")
    res = f"{c['name']}. " + ". ".join(partes)
    if len(res) > 250:
        res = f"{c['name']}. " + ". ".join(partes[:2]) + f". E mais {len(partes) - 2} mudanças no comparador"
    return True, assin, res


def regra_dm(f, mes):
    if str(f.get("DM", "")).strip() != "1" or f.get("DM_ULTIMO") == mes:
        return None
    return True, mes, ""


MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]


def resumo_mensal():
    """HTML do resumo mensal: melhores taxas por prazo hoje e o que mudou face à verificação de há cerca de um mês."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import gerar_indice as gi
    from datetime import date
    snaps = gi.carregar()
    hoje_dt, atual = snaps[-1]
    d0 = date.fromisoformat(hoje_dt)
    base = snaps[0]
    for dt, d in snaps:
        if (d0 - date.fromisoformat(dt)).days >= 25:
            base = (dt, d)
    est = gi.estado(atual)["prazos"]
    alt = gi.alteracoes(base[1], atual)
    nomes = {"3": "3 meses", "6": "6 meses", "12": "12 meses", "24": "24 meses"}
    linhas = ""
    for p in ("3", "6", "12", "24"):
        e = est.get(p)
        if not e:
            continue
        m, ms = e["melhor"], e["melhor_sem_condicoes"]
        linhas += (f'<tr><td style="padding:12px;border-top:1px solid #e9ecf1;color:#3a4454">{nomes[p]}</td>'
                   f'<td style="padding:12px;border-top:1px solid #e9ecf1"><b style="font-size:17px;color:#202432">{pct(m["tanb"])}</b><br><span style="font-size:13px;color:#697386">{m["banco"]}{" (novos clientes)" if m.get("novos") else ""}</span></td>'
                   f'<td style="padding:12px;border-top:1px solid #e9ecf1"><b style="font-size:17px;color:#202432">{pct(ms["tanb"])}</b><br><span style="font-size:13px;color:#697386">{ms["banco"]}</span></td></tr>')
    tabela = ('<table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;border-collapse:separate;border:1px solid #e9ecf1;border-radius:12px;font-size:15px;margin:0 0 28px">'
              '<tr style="text-align:left;color:#697386;font-size:12px;text-transform:uppercase;letter-spacing:.04em">'
              '<td style="padding:10px 12px;background:#f9fafb;border-radius:12px 0 0 0">Prazo</td><td style="padding:10px 12px;background:#f9fafb">Melhor taxa</td><td style="padding:10px 12px;background:#f9fafb;border-radius:0 12px 0 0">Sem condições</td></tr>' + linhas + "</table>")

    def lista(itens, n, fmt):
        return "".join(f'<li style="margin:0 0 6px">{fmt(x)}</li>' for x in itens[:n])
    mud = ""
    if alt["subidas"]:
        mud += f'<p style="{H3}">Subiram</p><ul style="margin:0 0 18px;padding-left:20px;font-size:15px;line-height:1.5;color:#3a4454">' + lista(alt["subidas"], 5, lambda x: f'{x["banco"]}, {x["produto"]} a {x["prazo"]} meses: {pct(x["antes"])} para <b>{pct(x["depois"])}</b>') + "</ul>"
    if alt["descidas"]:
        mud += f'<p style="{H3}">Desceram</p><ul style="margin:0 0 18px;padding-left:20px;font-size:15px;line-height:1.5;color:#3a4454">' + lista(alt["descidas"], 5, lambda x: f'{x["banco"]}, {x["produto"]} a {x["prazo"]} meses: {pct(x["antes"])} para <b>{pct(x["depois"])}</b>') + "</ul>"
    if alt["entraram"]:
        mud += f'<p style="{H3}">Novos no comparador</p><ul style="margin:0 0 18px;padding-left:20px;font-size:15px;line-height:1.5;color:#3a4454">' + lista(alt["entraram"], 5, lambda x: x) + "</ul>"
    if alt["sairam"]:
        mud += f'<p style="{H3}">Deixaram de estar disponíveis</p><ul style="margin:0 0 18px;padding-left:20px;font-size:15px;line-height:1.5;color:#3a4454">' + lista(alt["sairam"], 5, lambda x: x) + "</ul>"
    if not mud:
        mud = f'<p style="{P}">Nenhuma taxa mudou neste período.</p>'
    b = base[0].split("-")
    mes_txt = MESES[d0.month - 1]
    html = moldura(
        f'<h1 style="{H1}">Depósitos a prazo: as melhores taxas de {mes_txt}</h1>'
        f'<p style="{P}">Taxas verificadas a {d0.day} de {mes_txt} de {d0.year} junto de cada banco, para 10.000€. A melhor taxa pode exigir ser novo cliente. A coluna sem condições mostra a melhor sem essa exigência.</p>'
        + tabela +
        f'<h2 style="{H2}">O que mudou desde {int(b[2])} de {MESES[int(b[1]) - 1]}</h2>' + mud +
        botao_html("Ver todos os depósitos", f"{SITE}/comparador-depositos-a-prazo") +
        f'<p style="{NOTA}">Confirma sempre as condições no site do banco antes de subscrever.</p>',
        'Recebes este email porque pediste o resumo mensal de depósitos a prazo no Literacia Financeira. '
        f'<a href="*|UNSUB|*" style="color:{CINZA};text-decoration:underline">Cancelar</a>. Esta informação não é aconselhamento financeiro.')
    return f"{d0.year}-{d0.month:02d}", f"Depósitos a prazo: as melhores taxas de {mes_txt}", html


# ---------- emails ----------

LOGO = "https://franklinsilvapt-arch.github.io/depositos-comparator/email/logo-lf.png"
LARANJA, ESCURO, TEXTO, CINZA, LINHA = "#ff5a1f", "#202432", "#3a4454", "#697386", "#e9ecf1"
SERIF = "'Tiempos Headline',Georgia,'Times New Roman',serif"
SANS = "Inter,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
H1 = f"margin:0 0 14px;font-family:{SERIF};font-size:28px;line-height:1.2;font-weight:400;color:{ESCURO}"
H2 = f"margin:8px 0 14px;font-family:{SERIF};font-size:21px;line-height:1.25;font-weight:400;color:{ESCURO}"
H3 = f"margin:0 0 6px;font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:.04em;color:{CINZA}"
P = f"margin:0 0 22px;font-size:16px;line-height:1.55;color:{TEXTO}"
NOTA = f"margin:0;font-size:14px;line-height:1.5;color:{CINZA}"


def botao_html(texto, url):
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin:4px 0 26px"><tr><td style="background:{LARANJA};border-radius:12px">'
            f'<a href="{url}" style="display:inline-block;padding:14px 22px;font-family:{SANS};font-size:16px;font-weight:600;color:#ffffff;text-decoration:none">{texto} &rarr;</a></td></tr></table>')


def moldura(conteudo, rodape):
    """Layout comum dos emails, com o logótipo, as cores e os tipos de letra do Literacia Financeira."""
    return (
        f'<div style="margin:0;padding:32px 12px;background:#f9fafb;font-family:{SANS};color:{TEXTO}">'
        '<table role="presentation" cellpadding="0" cellspacing="0" align="center" style="width:100%;max-width:580px;margin:0 auto">'
        f'<tr><td style="padding:0 4px 20px"><a href="{SITE}" style="text-decoration:none"><img src="{LOGO}" width="200" height="15" alt="Literacia Financeira" style="display:block;border:0;width:200px;height:auto"></a></td></tr>'
        f'<tr><td style="background:#ffffff;border:1px solid {LINHA};border-radius:16px;padding:0">'
        f'<div style="height:4px;background:{LARANJA};border-radius:16px 16px 0 0;font-size:0;line-height:0">&nbsp;</div>'
        f'<div style="padding:30px 26px 28px">{conteudo}'
        f'<p style="margin:26px 0 0;padding-top:20px;border-top:1px solid {LINHA};font-size:14px;line-height:1.5;color:{TEXTO}">Obrigado,<br><b style="color:{ESCURO}">Equipa Literacia Financeira</b></p></div></td></tr>'
        f'<tr><td style="padding:20px 16px 0;font-size:12px;line-height:1.6;color:{CINZA};text-align:center">{rodape}<br>*|LIST:ADDRESSLINE|*</td></tr>'
        '</table></div>'
    )


def corpo(titulo, intro, destaque, botao, url, nota, motivo):
    return moldura(
        f'<h1 style="{H1}">{titulo}</h1>'
        f'<p style="{P}">{intro}</p>'
        f'<div style="background:#fff4ed;border-left:4px solid {LARANJA};border-radius:12px;padding:18px 20px;margin:0 0 26px;font-size:17px;line-height:1.45;font-weight:600;color:{ESCURO}">{destaque}</div>'
        + botao_html(botao, url) +
        f'<p style="{NOTA}">{nota}</p>',
        f'Recebes este email porque criaste um alerta {motivo} no Literacia Financeira. '
        f'<a href="*|UPDATE_PROFILE|*" style="color:{CINZA};text-decoration:underline">Mudar o critério</a> ou <a href="*|UNSUB|*" style="color:{CINZA};text-decoration:underline">cancelar o alerta</a>. '
        'Esta informação não é aconselhamento financeiro.')


def emails(data_txt):
    return {
        "dp": dict(
            assunto="Há um depósito a prazo com a taxa que pediste", previa="*|DP_RES|*",
            html=corpo("Encontrámos um depósito que cumpre o teu alerta",
                       f"Na verificação de {data_txt} há um depósito a *|DP_PRAZO|* meses com TANB de pelo menos *|DP_TAXA|*%, a taxa que pediste no teu alerta:",
                       "*|DP_RES|*", "Ver no comparador", f"{SITE}/comparador-depositos-a-prazo",
                       "Confirma as condições no site do banco antes de subscrever.", "de depósitos a prazo")),
        "el": dict(
            # Um só email para o comparador e para o índice (o tipo de casa do índice passa a consumo, em base_perfil_el).
            assunto="Há uma oferta de eletricidade mais barata para ti", previa="*|EL_RES|*",
            html=corpo("Encontrámos uma oferta mais barata para o teu consumo",
                       "Com os preços publicados pela ERSE, há uma oferta de preço fixo mais barata do que a melhor que havia quando criaste o alerta.",
                       "*|EL_RES|*", "Simular com o meu consumo", f"{SITE}/comparador-eletricidade",
                       "O valor inclui IVA, taxas e descontos para novos clientes. Confirma as condições no site do comercializador antes de mudar.", "de eletricidade")),
        "eu": dict(
            assunto="A Euribor mudou: vê o impacto na tua prestação", previa="*|EU_RES|*",
            html=corpo("A Euribor mudou",
                       "A Euribor a *|EU_PRAZO|* meses mudou o suficiente para disparar o teu alerta.",
                       "*|EU_RES|*", "Ver o impacto na prestação", f"{SITE}/simulador-euribor-prestacao",
                       "A prestação só muda na próxima revisão do teu crédito, com a Euribor dessa data.", "da Euribor")),
        "co": dict(
            assunto="A corretora que segues mudou os custos", previa="*|CO_RES|*",
            html=corpo("A corretora que segues mudou",
                       "Na última revisão dos preçários encontrámos mudanças na corretora do teu alerta.",
                       "*|CO_RES|*", "Ver a corretora no comparador", f"{SITE}/comparador-de-corretoras",
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
    for t, url in (("el", URL_EL), ("elo", URL_EL_OFERTAS), ("eu", URL_EU), ("co", URL_CO)):
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
        for t in ("dm", "dp", "el", "eu", "co"):
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

    mes_dm, assunto_dm, html_dm = resumo_mensal()
    regras = {"dm": lambda f: regra_dm(f, mes_dm),
              "dp": lambda f: regra_dp(f, fontes["dp"]),
              "el": lambda f: regra_el_consumo(f, fontes["elo"]) if "elo" in fontes else None,
              "eu": lambda f: regra_eu(f, fontes["eu"]) if "eu" in fontes else None,
              "co": lambda f: regra_co(f, fontes["co"], mud) if "co" in fontes else None}
    marcados = {t: [] for t in regras}
    for m in membros:
        f = m.get("merge_fields", {})
        b = base_perfil_el(f, fontes["elo"]) if "elo" in fontes else None
        if b:
            print(("[simulação] " if SIMULAR else "") + f"[el] {m['email_address']}: referência do tipo de casa gravada ({b['EL_MES']}€ por mês)")
            f.update(b)
            if not SIMULAR:
                mc.req("PATCH", f"/lists/{lst}/members/{m['id']}", {"merge_fields": b})
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
            if avisar and res:
                patch[f"{pre}_RES"] = res[:255]
            mc.req("PATCH", f"/lists/{lst}/members/{m['id']}", {"merge_fields": patch})
            if avisar:
                mc.etiqueta(m["id"], f"alerta-{t}-envio", True)
                marcados[t].append(m["id"])

    print(f"{len(membros)} contactos; a avisar: " + ", ".join(f"{t}={len(v)}" for t, v in marcados.items()))
    # Registo da execução (sem emails), para se ver no repositório o que aconteceu sem abrir os logs do GitHub.
    from datetime import datetime, timezone
    reg = {"execucao": datetime.now(timezone.utc).isoformat(timespec="seconds"), "contactos": len(membros),
           "por_tipo": {t: sum(1 for m in membros if any(str((m.get("merge_fields") or {}).get(k, "")).strip() for k in chaves))
                        for t, chaves in {"dm": ["DM"], "dp": ["DP_PRAZO"], "el": ["EL_PERFIL", "EL_KWH"], "eu": ["EU_PRAZO"], "co": ["CO_ID"]}.items()},
           "a_avisar": {t: len(v) for t, v in marcados.items()}, "campanhas": {}}
    if not SIMULAR:
        (ROOT / "data/alertas").mkdir(parents=True, exist_ok=True)
    if SIMULAR:
        return
    gravar_registo(reg)
    d = deps["meta"]["data_verificacao"].split("-")
    textos = emails(f"{d[2]}/{d[1]}/{d[0]}")
    textos["dm"] = dict(assunto=assunto_dm, previa="As melhores taxas por prazo e o que subiu ou desceu no último mês.", html=html_dm)
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
        reg["campanhas"][t] = camp["id"]
        gravar_registo(reg)



def gravar_registo(reg):
    (ROOT / "data/alertas").mkdir(parents=True, exist_ok=True)
    (ROOT / "data/alertas/ultima-execucao.json").write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
