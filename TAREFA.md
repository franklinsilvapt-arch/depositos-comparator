# Tarefa quinzenal: verificar os depósitos a prazo do comparador

Corre nos dias 1 e 16 de cada mês (ou quando o Franklin pedir). O dia 1 apanha o Excel novo do Economia e Finanças; o dia 16 apanha as mudanças de meio de mês nos sites dos bancos. O objetivo é um relatório
curto que o Franklin aprova em 10 minutos. Nunca alterar `data/depositos.json`
sem aprovação explícita.

## Passos

1. Correr `python3 scripts/verificar_depositos.py`. Gera `verificacao/AAAA-MM/relatorio.md`,
   `economiafinancas.json` (todas as linhas do Excel) e `paginas/` (texto de cada site).
2. Ler a secção 2b (catálogos dos bancos). Para cada nome candidato com taxa >= 2,00%,
   abrir a página guardada em `paginas/catalogo-*.txt` e confirmar se é um depósito a prazo
   para particulares. Se for, recolher TANB por prazo, mínimo, máximo, mobilização, IRS e
   link da FIN, e propor a inclusão na lista "Novo". Os grandes bancos (CGD, BPI, BCP,
   Santander, Novo Banco, Crédito Agrícola, Montepio, Abanca) estão nos catálogos mesmo
   sem produtos na lista: quase nunca chegam aos 2,00%, mas quando lançam campanhas é aqui
   que aparecem.
3. Para cada linha marcada com ⚠️ ou "sem correspondência", ler o texto guardado em
   `paginas/` e, se existir, a FIN (`url_fin`). Procurar a TANB do prazo em causa,
   o montante mínimo e a regra de mobilização antecipada. Se a página não tiver a
   taxa (o Haitong, por exemplo, só a publica no preçário), dizer isso e apontar onde
   confirmar à mão.
4. Abrir o post do JRJordao no Fórum do Investidor
   (https://forumdoinvestidor.pt/viewtopic.php?p=4319#p4319), ver a data de
   "Última atualização" e a imagem da tabela. Anotar qualquer taxa diferente da nossa
   ou oferta nova com TANB >= 2,50% que não esteja no Excel nem no nosso JSON.
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
   - registar a verificação no registo de dados vivos do Notion.

## Regras

- Uma taxa só muda no JSON com uma fonte primária (site do banco, FIN ou preçário).
  O Excel e o fórum servem para apanhar mudanças, não para as confirmar.
- Nunca citar nem usar dados da DECO PROteste. Se o Excel tiver linhas com bonificação
  "DECO", ignorar essas linhas e usar a taxa base do banco.
- Depósitos só para menores (ex.: BK Mini do Bankinter) ficam de fora.
- Se uma oferta nova tiver TANB >= 2,00% e for subscritível por qualquer particular,
  propor a inclusão. Abaixo de 2,00% não entra.
- Números em formato pt-PT no relatório (2,75%, 5.000€).
