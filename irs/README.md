# Tabelas de IRS (literaciafinanceira.pt)

- `tabelas-irs.js`: desenha a página dentro de `#lf-dp` (calculadora de escalão, escalões de IRS e tabelas de retenção I a III do continente). Reutiliza `../comparador-depositos.css`.
- `tabelas-irs.css`: suplemento de estilos.

Os valores estão no topo do `tabelas-irs.js` e têm de ser atualizados à mão quando a lei muda:

- Escalões: artigo 68.º do Código do IRS, redação da Lei n.º 73-A/2025 (OE 2026).
- Retenção na fonte: Despacho n.º 233-A/2026, de 6 de janeiro (Tabelas I, II e III).
- IAS 2026: 537,13€. Mínimo de existência: 12.880€.

Pendente a 30/09/2026: proposta de lei entregue no Parlamento a 21/09/2026 para baixar as taxas do 1.º ao 6.º escalão, com novas tabelas de retenção previstas para novembro. Quando for publicada, atualizar `ESC`, `MEDIA`, `RET`, `VERIFICADO` e o aviso.
