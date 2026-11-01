# Verificação dos depósitos a prazo - 2026-11-01

Verificação quinzenal feita por sessão agendada na cloud. Base: `data/depositos.json` com
`meta.data_verificacao` a 2026-10-16 e 75 entradas. Nada foi alterado em nenhum ficheiro de dados.

## Contexto: taxa do BCE

A taxa de facilidade de depósito do BCE está nos **2,50%** e ficou inalterada na reunião de
29 de outubro de 2026 (página de taxas oficiais do BCE, publicada a 2026-10-28). Como não mudou
desde a verificação de 16 de outubro, não há razão sistémica para rever as taxas variáveis desta
lista. As mudanças desta quinzena são de campanha, não de mercado.

Nota: a leitura automática da tabela do BCE ficou truncada a meio e a parte dos valores veio de um
resumo, não do texto da própria tabela. O valor de 2,50% é consistente com o comunicado da reunião
de 29 de outubro, mas vale um olhar de confirmação antes de servir de base a qualquer alteração.

## O GitHub Action desta manhã não produziu relatório

O workflow `verificar-depositos.yml` está agendado para `0 7 1,16 * *`, ou seja 07:00 UTC de hoje.
Às 08:45 UTC não existia `verificacao/2026-11-01/`, não havia commit novo no repo (o último é de
2026-10-31, "Alertas: guardar estado das corretoras") e não havia issue nova com a etiqueta
`verificacao-mensal` (a mais recente continua a ser a #5, de 2026-10-16). Por isso esta verificação
foi feita sem o `economiafinancas.json` nem as páginas guardadas em `paginas/`, que é o que explica
a lista comprida em "Não consegui confirmar" mais abaixo.

Convém ver o histórico de execuções do workflow nos Actions. Se falhou, o passo mais provável é o
`pip install` ou o `verificar_depositos.py` a bater num 403.

## Resumo

### Mudou

Nada confirmado. Dos oito sites de bancos com as taxas mais altas, só o Banco Finantia e o
Bison Bank abriram, e em ambos as taxas que temos guardadas continuam iguais às publicadas
(site do Finantia, página atualizada a 2026-10-14, e site do Bison Bank, página atualizada a
2026-10-26).

### Novo

- **Bison Bank, Depósito a Prazo Bison Growth**, 12 meses, TANB 3,00%. Montantes entre 25.000€ e
  500.000€, só para novos recursos, mobilização antecipada com penalização de 100% dos juros,
  coberto pelo FGD até 100.000€. Só está publicado o prazo de 12 meses. Entra na regra de inclusão,
  TANB igual ou superior a 1% e subscritível por particulares (site do Bison Bank,
  bisonbank.com/pt/depositos-a-prazo, 2026-11-01).

### Para corrigir no que já lá está

- **Banco Finantia, DP Visão**: o site publica duas variantes a 24 meses, ambas com TANB 3,15% e
  ambas de 50.000€ a 500.000€. Uma é "Mobilização Antecipada", com juros no vencimento e resgate a
  qualquer momento com penalização. A outra é "Mobilização Semestral", com juros semestrais e
  resgate só nas datas de juros, com aviso de sete dias. Temos uma só linha, com
  `mobilizacao: parcial`. Decidir se queremos as duas ou se a nota basta (site do Finantia,
  2026-11-01).
- **Bison Bank, DP Bison Rendimento Premium**: as taxas confirmam-se, 3,00% a 3, 6, 12 e 24 meses,
  mínimo 5.000€ e máximo 250.000€, mobilização com penalização de 100% dos juros, renovação
  automática à taxa Standard. Mas o `url` que temos guardado,
  `bisonbank.com/pt-pt/servicos-de-private-banking/dp-bison-rendimento-premium/`, não foi o que
  respondeu. A página que abriu foi
  `bisonbank.com/pt-pt/servicos-de-private-banking/depositos-a-prazo-rendimento-premium-bison-bank/`.
  Parece que o endereço mudou e o nosso está desatualizado. Vale confirmar num clique.
- O site do Bison Bank acrescenta uma restrição que não temos registada neste produto: conta de um
  só titular e exclusivo a cidadãos portugueses com Cartão de Cidadão válido e residentes no EEE.

### Desapareceu

Nada confirmado. A página `bisonbank.com/pt/depositos-a-prazo/` só mostra hoje o Bison Growth e já
não mostra o Rendimento Premium, mas este continua a existir no seu próprio endereço, por isso não
é um produto que tenha saído, é a página de entrada que mudou de destaque.

### Não consegui confirmar

Os sites dos bancos portugueses bloqueiam leitura automática de forma generalizada, exatamente como
no relatório de 16 de outubro. Nenhuma destas entradas foi reconfirmada nesta passagem e nenhuma
delas é por isso uma mudança, apenas falta de leitura:

- **Banco BiG** (Super Depósito 3m 4,00% e 6m 3,50%, Depósito GO, Novos Montantes 3 Meses): a
  página responde 200 mas com o conteúdo de erro do próprio site, "This page can't be displayed".
- **Banco Best, Banco Carregosa, BAI Europa, Banco Invest, Haitong Bank**: erro de cliente na
  leitura, sem conteúdo. No Carregosa isto é especialmente pena, porque é onde está a campanha de
  Natal (Depósito Natal e NextGen Christmas Greetings, 3m 2,50%, 6m 2,75% e 12m 3,00%) e é a época
  do ano em que ela muda.
- **Caixa Geral de Depósitos**: o endereço que temos,
  `cgd.pt/Particulares/Poupanca-Investimento/Depositos-Prazo/Pages/Depositos-Prazo.aspx`, devolve a
  página de erro da CGD, "ESTA PÁGINA NÃO EXISTE", com status 200. O endereço mudou e tem de ser
  encontrado de novo a partir da página inicial.
- **Banco Montepio, BPI, Novo Banco, Santander**: erro de cliente na leitura.
- **Millennium bcp**: o robots.txt do banco bloqueia leitura automática desta página. É
  verificação à mão.
- **Economia e Finanças**: o Excel não foi lido porque o Action não correu. No relatório de 16 de
  outubro o site devolveu 403.
- **Fórum do Investidor, post do JRJordao**: a tabela é imagem e o fórum bloqueia pedidos
  automáticos. Fica para o teu clique em
  `forumdoinvestidor.pt/viewtopic.php?p=4319#p4319`.
- **Catálogos dos grandes bancos**: não houve passagem pelos catálogos (CGD, BPI, BCP, Santander,
  Novo Banco, Crédito Agrícola, Montepio, Abanca) porque nenhum abriu. Em outubro a CGD tinha 2,60%
  a 6 meses, o Montepio 2,70% a 6 meses e o BPI 2,50% a 6 meses, e campanhas de fim de ano nestes
  bancos são frequentes. Esta é a parte que mais vale a pena olhar à mão nesta quinzena.

## Próximo passo

Nada a alterar sem o teu ok. Quando aprovares, o que entra em `data/depositos.json` é a entrada nova
do Bison Growth, a correção do `url` do Rendimento Premium e a decisão sobre as duas variantes do
DP Visão, mais `meta.data_verificacao`. O resto da lista continua com a data de 2026-10-16 porque
não foi reconfirmado.
