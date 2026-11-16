# Verificação dos depósitos a prazo - 2026-11-16

Verificação quinzenal da sessão de chat. Base: `data/depositos.json` com `meta.data_verificacao` a 2026-11-01, 85 entradas.
Nada foi alterado nos dados. Isto é só o relatório.

## Aviso: o GitHub Action de hoje não correu

A esta hora (08:40 UTC de 2026-11-16) não existe `verificacao/2026-11-16/`, não há issue nova com a etiqueta
`verificacao-mensal` e o último commit no repo é de 2026-11-15 às 17:22 UTC ("Alertas: guardar estado das corretoras").
O workflow devia ter corrido às 07:00 UTC e produzido o relatório mais a issue. As três issues existentes são a #7
(2026-11-01), a #5 (2026-10-16) e a #2 (2026-10-01), todas abertas.

Consequência prática: esta ronda não tem `economiafinancas.json`, não tem `paginas/` e não tem a leitura dos preçários
em PDF pelo `verificar_precarios.py`. Essa leitura é a parte que funciona melhor, porque os sites dos bancos bloqueiam
leitura automática e os preçários não. Sem ela, a verificação de hoje assenta só no que se consegue ler dos sites.
Vale a pena ver os logs do workflow e, se for caso disso, lançar um dispatch à mão.

## Taxa de facilidade de depósito do BCE

Sem alteração desde a última verificação, e é esse o ponto de partida de tudo o resto.

- Em vigor: 2,50%, com efeito a 16 de setembro de 2026. Antes disso 2,25%, com efeito a 17 de junho de 2026
  (tabela das taxas diretoras do BCE).
- A última conferência de imprensa de política monetária foi a 29 de outubro de 2026 e não há registo de alteração
  da taxa nessa data. A tabela do BCE não tem nenhuma entrada posterior a 16 de setembro de 2026.
- O calendário do BCE não mostra nenhuma reunião de política monetária entre 29 de outubro e 16 de dezembro de 2026.
  A próxima é a 16 e 17 de dezembro de 2026, com conferência de imprensa a 17.

Ou seja, entre 1 de novembro e hoje não houve movimento do BCE. Era de esperar que as taxas variáveis destas listas
estivessem paradas, e em geral é isso que se confirma abaixo.

## Mudou

- Klarna, Conta poupança a prazo fixo: os prazos curtos subiram na tabela portuguesa da Klarna. 3 meses de 1,84% para
  2,29%, 6 meses de 2,15% para 2,42%. O prazo de 9 meses, que no nosso ficheiro não existe nesta entrada mas existe no
  comparador de poupanças, está a 2,54%. De 12 meses para cima está igual: 12 meses 2,95%, 24 meses 3,15%
  (klarna.com/pt/conta-poupanca, lido a 2026-11-16).
  Atenção a uma incoerência na própria página: a tabela dá 2,29% a 3 meses, mas uma nota de pé de página continua a
  dizer que as taxas garantidas vão de "1,84% e 3.24%" para 3 a 48 meses, o que é exatamente o nosso valor antigo.
  A tabela é o que o cliente vê e subscreve, mas isto merece um olhar antes de entrar.

Mais nada mudou nas entradas que se conseguiram ler.

## Confirmado sem alteração

- Banco BiG, Super Depósito: 3 meses 4,00% com mínimo de 5.000€, 6 meses 3,50% com mínimo de 10.000€, máximo de
  50.000€, exclusivo de novos clientes (big.pt/TaxasDepositos/DepositosPrazo, lido a 2026-11-16). Igual ao ficheiro.
- Haitong Bank, HB Sem Mobilização: 3 meses 3,05%, 6 meses 3,20%, 12 meses 3,25%, 24 meses 3,30%, sem limite mínimo
  nem máximo (site do Haitong, lido a 2026-11-16). Igual.
- Haitong Bank, HB Com Mobilização: 3 meses 3,00%, 6 meses 3,15%, 12 meses 3,20%, 24 meses 3,25% (idem). Igual.
- Haitong Bank, Depósito Premium: variante mobilizável 6 meses 3,25%, 12 meses 3,30%, 24 meses 3,35%, mínimo de
  50.000€ (idem). Igual.
- Haitong Bank, Depósito Premium Não Mobilizável: 3 meses 3,15%, 6 meses 3,30%, 12 meses 3,35% (idem). Igual.
- BAI Europa, Depósito a Prazo Não Mobilizável: 3 meses 2,60%, 6 meses 3,15%, 12 meses 3,25%, não renovável, sem
  mobilização antecipada (site do BAI Europa, lido a 2026-11-16). Igual.
- Banco Finantia, DP Jump: 6 meses 3,00%, 12 meses 3,10%, mínimo de 50.000€, exclusivo para novos montantes, sem
  mobilização antecipada (finantia.com, página alterada a 2026-10-14, lida a 2026-11-16). Igual.
- Banco Finantia, DP Visão: 24 meses 3,15% (idem). Igual.
- Banco Finantia, Depósito Mobilizável: 6 meses 2,55%, 12 meses 2,65%, 24 meses 2,70% (idem). Igual.
- Banco Finantia, Depósito Não Mobilizável: 6 meses 2,80%, 12 meses 2,90%, 24 meses 2,95% (idem). Igual.
- BNI Europa, Depósito a Prazo Não Mobilizável: 6 meses 2,70%, 12 meses 2,75%, 24 meses 3,00%, mínimo de 2.500€
  (bnieuropa.pt, página alterada a 2026-10-29, lida a 2026-11-16). Igual.
- BNI Europa, Depósito a Prazo Mobilizável: 3 meses 2,55%, 6 meses 2,55%, 12 meses 2,65%, 24 meses 2,75% (idem). Igual.
- BNI Europa, DP Juros Mensais: 6 meses 2,65%, 12 meses 2,70%, 24 meses 2,95% (idem). Igual.
- Banco Best, Depósito Novos Clientes: 6 meses 3,30%. Ver a ressalva na secção seguinte.

## Candidatos novos, por confirmar

Nenhum destes entra sem uma segunda leitura. São pistas, não confirmações.

- Banco Best, "Depósito Novos Clientes Aniversário": 180 dias, TANB 3,30%, mínimo de 500€, máximo de 250.000€ por
  cliente e por conta, não renovável, sem reforços, juros no vencimento, mobilização antecipada com penalização total
  de juros, um depósito por morada, não acumulável com outras campanhas de novos clientes. Isto bate com os nossos
  3,30% a 6 meses, mas o nome é diferente do que temos e a leitura da página do Best veio truncada, com a tabela a
  cair fora da parte lida em texto verdadeiro. Confirmar o nome do produto e as condições na página ou na FIN antes de
  mexer na entrada (bancobest.pt/ptg/best_deposito-prazo-novos-clientes, leitura parcial a 2026-11-16).
- Banco BiG, produtos que não temos na lista e que a página mostra em euros: Depósito GO 6 meses 2,75% (5.000€ a
  250.000€), Novos Montantes 3 meses 2,75% (5.000€ a 500.000€), Dep. a Prazo TOP 3 meses 1,75%, 6 meses 2,00%,
  12 meses 2,25% (mínimo de 50.000€), Depósito a Prazo 3 meses 1,50%, 6 meses 1,75%, 1 ano 2,00% (mínimo de 1.000€),
  Renda Mensal 6 meses 1,85% e 12 meses 2,10% (mínimo de 10.000€). Todos acima de 1,00% e aparentemente subscritíveis
  por qualquer particular, logo candidatos à regra de inclusão. Decidir se entram ou se há uma razão anterior para
  ficarem de fora (big.pt, lido a 2026-11-16).
- Banco Finantia: a página tem o DP Jump com banner de campanha mas sem data de fim indicada. Nada a mudar, fica como
  nota para a próxima ronda.
- Scalable Capital, Festgeld: a página alemã publica também um prazo de 6 meses a 2,75% que não temos. Fora do âmbito
  deste ficheiro, fica registado para o comparador de poupanças.

## Desapareceu

Nada. Nenhuma entrada da lista deixou de constar das fontes que se conseguiram abrir.

## Não consegui confirmar

Precisa de um clique do Franklin, ou de uma corrida do Action com o `verificar_precarios.py`.

- Economia e Finanças: não foi lido nesta ronda. Na ronda de 1 de novembro já tinha devolvido 403.
  Verificar à mão em economiafinancas.com/taxas-de-juro-depositos-a-prazo.
- Fórum do Investidor, post do JRJordao: a tabela é uma imagem e o fórum bloqueia pedidos automáticos.
  Abrir forumdoinvestidor.pt/viewtopic.php?p=4319#p4319 e comparar a data de última atualização.
- Banco Carregosa: a página do Depósito Bem-Vindo devolveu erro de cliente. Ficam sem confirmação os 3 meses 3,00% e
  6 meses 2,80% do Bem-Vindo e do NextGen Welcome Boost, e também as restantes nove entradas do Carregosa, incluindo
  o Depósito Natal e o NextGen Christmas Greetings, que são de campanha e por isso os que mais arriscam ficar velhos.
- ActivoBank: a página de depósitos devolveu HTTP 200 com um corpo de 13 caracteres, sem conteúdo legível. Ficam sem
  confirmação o Depósito Novos Clientes AB (3 meses 3,00%), o Depósito Dinheiro Novo AB (3 meses 3,00%) e o Depósito
  Dinheiro Novo Plus AB (6 meses 2,60%).
- Banco Invest: a página abriu mas a lista de produtos não renderizou. O texto ainda tem os marcadores do template
  (`${singleRate}`, `${description}`) e a mensagem "Serviço temporariamente indisponível. Por favor tente mais tarde."
  Fica sem confirmação o Choice Novos Montantes (3, 6 e 12 meses a 2,75%). Vale a pena repetir mais tarde, a página
  estava em estado quebrado e não necessariamente desatualizada.
- Caixa Geral de Depósitos: a página de depósitos a prazo que temos devolve "ESTA PÁGINA NÃO EXISTE" com HTTP 200.
  O URL mudou. Encontrar o novo e atualizar a lista de catálogos.
- Montepio, BPI, Bison Bank, Bankinter: erro de cliente permanente, não foi possível ler nenhuma. Ficam sem
  confirmação, entre outras, o Bankinter Depósito Net Boas Vindas (6 meses 3,00%), o Bison Bank DP Bison Rendimento
  Premium (3, 6, 12 e 24 meses a 3,00%) e o Bison Growth (12 meses 3,00%).
- BAI Europa, Depósito Novos Clientes e Depósito a Prazo Premium EUR: as páginas próprias não foram abertas nesta
  ronda. A entrada do Não Mobilizável foi confirmada e as outras duas ficam por confirmar.
- Preçários em PDF: nenhum foi lido, porque esta sessão não corre o `verificar_precarios.py`. É aqui que está a
  confirmação vinculativa de BiG, Best, Carregosa, BAI, Invest, Haitong, Montepio, BPI, Novo Banco e Santander.

## Nota sobre outro ficheiro deste repo

Nada a fazer aqui, só para contexto: o commit de 2026-11-13 ("Anúncio da Trade Republic: 4% até 20.000€ para novos
clientes, até 01/03/2027", PR #13) já está no repo. A campanha da Trade Republic continua a constar dos dados dos
comparadores do eupersonalfinance.eu com a mesma data de fim.

## Próximo passo

Rever este relatório. Depois do "ok", e só depois, escrever os patches em `verificacao/2026-11-16/` e aplicar pelo
dispatch do `aplicar-alteracoes.yml`, com `data_verificacao` incluído no patch. A única alteração com fonte primária
pronta a entrar é a da Klarna, e mesmo essa com a ressalva da nota de pé de página. Antes disso vale mais a pena
descobrir porque é que o Action não correu, porque sem os preçários esta ronda fica muito mais fraca do que o normal.
