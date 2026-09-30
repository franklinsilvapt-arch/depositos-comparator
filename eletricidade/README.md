# Comparador de eletricidade (literaciafinanceira.pt)

Ficheiros servidos pelo GitHub Pages deste repositório, em `/depositos-comparator/eletricidade/`.

- `comparador-eletricidade.js`: o comparador. Desenha dentro de `#lf-dp` e reutiliza o CSS do comparador de depósitos (`../comparador-depositos.css`).
- `comparador-eletricidade.css`: suplemento de estilos só deste comparador.
- `data/ofertas.json`: ofertas de eletricidade (clientes domésticos, só eletricidade, potências de 1,15 a 20,7 kVA).
- `scripts/atualizar_ofertas.py`: gera `data/ofertas.json` a partir do ficheiro oficial da ERSE ("Ofertas comerciais (CSV)" em https://simuladorprecos.erse.pt/).
- `workflow-eletricidade-ofertas.yml`: workflow diário que corre o script. Para ficar ativo tem de ser copiado para `.github/workflows/eletricidade-ofertas.yml`.

## Dados

Fonte única: o ficheiro de ofertas comerciais que os comercializadores comunicam à ERSE e que alimenta o simulador de preços do regulador.
O `data/ofertas.json` inicial (29/09/2026) é parcial (`"parcial": true`): tem só as ofertas que podem ser a mais barata de cada comercializador. Quando o workflow correr, passa a ter todas.

## Cálculo da fatura

Segue a metodologia do simulador da ERSE e foi validado ao cêntimo nos consumidores-tipo (3,45 kVA com 1.900 kWh: 441,79€ na tarifa regulada bi-horária, 6,9 kVA com 5.000 kWh: 1.140,32€):

- energia e potência aos preços da oferta (sem IVA), 365 dias
- IVA a 6% nos primeiros 200 kWh por 30 dias (potências até 6,9 kVA) e 23% no resto
- IVA a 6% no termo fixo da tarifa de acesso às redes para potências até 3,45 kVA, 23% no resto da potência
- imposto especial de consumo: 0,001€/kWh, com IVA a 23%
- contribuição audiovisual: 2,85€/mês, com IVA a 6%
- descontos, reembolsos e serviços adicionais obrigatórios anualizados
- a taxa de exploração da DGEG (0,07€/mês) não entra, tal como no simulador da ERSE

Os valores regulados (termo fixo das tarifas de acesso, IEC, CAV) estão no topo do `comparador-eletricidade.js` e têm de ser revistos quando a ERSE publica novas tarifas (normalmente a 1 de janeiro).
