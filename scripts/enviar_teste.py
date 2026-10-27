"""Envia um exemplo de cada email de alerta (envio de teste do Mailchimp, sem tocar nos contactos da audiência).
Os campos de cada pessoa vêm preenchidos com exemplos calculados com os dados de hoje.
O endereço chega como input do workflow e é lido do ficheiro do evento (nunca escrito no YAML), mascarado nos registos."""
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import enviar_alertas as e  # noqa: E402


def cond(h, tem_kwh):
    return re.sub(r"\*\|IF:EL_KWH\|\*(.*?)\*\|ELSE:\|\*(.*?)\*\|END:IF\|\*", lambda m: m.group(1) if tem_kwh else m.group(2), h, flags=re.S)


def main():
    ev = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text()) if os.environ.get("GITHUB_EVENT_PATH") else {}
    para = (ev.get("inputs") or {}).get("email") or os.environ["TESTE_EMAIL"]
    print(f"::add-mask::{para}")
    key, lst = os.environ["MAILCHIMP_API_KEY"], os.environ["MAILCHIMP_LIST_ID"]
    mc = e.MC(key, lst)
    d = json.loads((e.ROOT / "data/depositos.json").read_text(encoding="utf-8"))["meta"]["data_verificacao"].split("-")
    T = e.emails(f"{d[2]}/{d[1]}/{d[0]}")
    _, ass_dm, html_dm = e.resumo_mensal()

    elo, el = e.get_json(e.URL_EL_OFERTAS), e.get_json(e.URL_EL)
    i = elo["pots"].index(6.9)
    r_elc = e.regra_el_consumo({"EL_POT": str(i), "EL_KWH": "3500", "EL_MES": "999"}, elo)
    r_eli = e.regra_el({"EL_PERFIL": "p2", "EL_MAX": "99999"}, el)
    exemplos = [
        ("Depósitos (comparador e índice)", ass_dm, html_dm, {}),
        ("Eletricidade (comparador)", T["el"]["assunto"], cond(T["el"]["html"], True), {"EL_RES": r_elc[2] if r_elc else ""}),
        ("Eletricidade (índice)", T["el"]["assunto"], cond(T["el"]["html"], False), {"EL_RES": r_eli[2] if r_eli else ""}),
        ("Corretoras", T["co"]["assunto"], T["co"]["html"], {"CO_RES": "DEGIRO. Câmbio: de 0,10% para 0,25%. Custódia (condições atualizadas)"}),
    ]
    for nome, assunto, html, campos in exemplos:
        for k, v in campos.items():
            html = html.replace(f"*|{k}|*", v)
        camp = mc.req("POST", "/campaigns", {
            "type": "regular", "recipients": {"list_id": lst},
            "settings": {"subject_line": assunto, "title": f"Teste: {nome}", "from_name": "Literacia Financeira",
                         "reply_to": os.environ.get("MAILCHIMP_FROM", "geral@literaciafinanceira.pt")}})
        try:
            mc.req("PUT", f"/campaigns/{camp['id']}/content", {"html": html})
            mc.req("POST", f"/campaigns/{camp['id']}/actions/test", {"test_emails": [para], "send_type": "html"})
            print(f"enviado: {nome}")
        finally:
            mc.req("DELETE", f"/campaigns/{camp['id']}")


if __name__ == "__main__":
    main()
