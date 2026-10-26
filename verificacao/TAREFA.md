# Tarefa quinzenal: verificar os depósitos a prazo do comparador

Corre nos dias 1 e 16 de cada mês (ou quando o Franklin pedir). O dia 1 apanha o Excel novo do Economia e Finanças; o dia 16 apanha as mudanças de meio de mês nos sites dos bancos. O objetivo é um relatório
curto que o Franklin aprova em 10 minutos. Nunca alterar `data/depositos.json`
sem aprovação explícita.

## Passos

1. Correr `python3 scripts/verificar_depositos.py`. Gera `verificacao/AAAA-MM-DD/relatorio.md`,
   `economiafinancas.json` (todas as linhas do Excel) e `paginas/` (texto de cada site).
2. Ler a secção 2b (catálogos dos bancos). Para cada nome candidato com taxa >= 1,00%,
   abrir a página guardada em `paginas/catalogo-*.txt` e confirmar se é um depósito a prazo
   para particulares. Se for, recolher TANB por prazo, mínimo, máximo, mobilização, IRS e
   link da FIN, e propor a inclusão na lista "Novo". Os grandes bancos (CGD, BPI, BCP,
   Santander, Novo Banco, Crédito Agrícola, Montepio, Abanca) estão nos catálogos mesmo
   sem produtos na lista, e lançam campanhas com regularidade: em outubro de 2026 a CGD
   tinha 2,60% a 6 meses, o Montepio 2,70% a 6 meses e o BPI 2,50% a 6 meses. Vale a pena
   percorrê-los sempre.
3. Para cada linha marcada com ⚠️ ou "sem correspondência", ler o texto guardado em
   `paginas/` e, se existir, a FIN (`url_fin`). Procurar a TANB do prazo em causa,
   o montante mínimo e a regra de mobilização antecipada. Se a página não tiver a
   taxa (o Haitong, por exemplo, só a publica no preçário), dizer isso e apontar onde
   confirmar à mão.
4. Abrir o post do JRJordao no Fórum do Investidor
   (https://forumdoinvestidor.pt/viewtopic.php?p=4319#p4319), ver a data de
   "Última atualização" e a imagem da tabela. Anotar qualquer taxa diferente da nossa
   ou oferta nova com TANB >= 1,00% que não esteja no Excel nem no nosso JSON.
5. Escrever o resumo final no topo de `relatorio.md`, nesta ordem:
   - **Mudou**: depósitos cuja TANB, mínimo ou mobilização mudou, com fonte e data.
   - **Novo**: ofertas a acrescentar, com TANB, prazo, mínimo, condições e link.
   - **Desapareceu**: depósitos que já não constam de nenhuma fonte.
   - **Não consegui confirmar**: o que precisa de um clique do Franklin.
   Cada linha com a fonte entre parênteses (Excel EF, site do banco, FIN, JRJordao).
6. Enviar o resumo ao Franklin. Só depois do "ok" dele:
   - editar `data/depositos.json` (taxas, notas, `url_fin`, `a_confirmar`, `meta.data_verificacao`),
   - atualizar a data "última verificação das taxas" na página do comparador e no
     artigo dos melhores depósitos a prazo,
   - registar a verificação no registo de dados vivos do Notion,
   - guardar o índice: copiar `data/depositos.json` para `data/historico/AAAA-MM-DD.json`
     (data de `meta.data_verificacao`), correr `python3 scripts/gerar_indice.py` e fazer
     commit de `data/historico/` e `data/indice.json` (o workflow `gerar-indice.yml` faz
     isto sozinho quando estiver ativo),
   - atualizar na página /indice-depositos-a-prazo do Webflow a primeira pergunta do
     glossário (melhor taxa e mediana a 12 meses do mês), que é texto fixo para o Google e as IAs,
   - no dia 1 de cada mês, confirmar no BPstat se o Banco de Portugal publicou uma nova média
     dos novos depósitos e atualizar `data/referencias.json`.

## Regras

- Uma taxa só muda no JSON com uma fonte primária (site do banco, FIN ou preçário).
  O Excel e o fórum servem para apanhar mudanças, não para as confirmar.
- Nunca citar nem usar dados da DECO PROteste. Se o Excel tiver linhas com bonificação
  "DECO", ignorar essas linhas e usar a taxa base do banco.
- Depósitos só para menores (ex.: BK Mini do Bankinter) ficam de fora.
- Se uma oferta nova tiver TANB >= 1,00% e for subscritível por qualquer particular,
  propor a inclusão. Abaixo de 1,00% não entra. Este é o mesmo limiar que está em
  `meta.regra_inclusao` no `data/depositos.json`: se um dos dois mudar, mudar o outro.
- Depósitos com limite de idade entram com a etiqueta "Até X anos" (campo `idade_max`),
  não ficam de fora. Só os que são exclusivos de menores é que ficam de fora.
- Depósitos que exigem domiciliação de ordenado ficam de fora.
- A grelha de prazos é 3, 6, 12 e 24 meses.
- Números em formato pt-PT no relatório (2,75%, 5.000€).
