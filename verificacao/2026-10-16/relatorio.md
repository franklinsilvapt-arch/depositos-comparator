# Verificação dos depósitos a prazo - 2026-10-16

Verificação quinzenal do dia 16. Base: `data/depositos.json` verificado a 2026-10-09, 58 entradas.

**Nada foi alterado.** Nem `data/depositos.json`, nem o Webflow, nem a data de verificação.
Este ficheiro é só o relatório.

## Nota sobre o GitHub Action

O Action das 07:00 UTC de hoje não produziu `verificacao/2026-10-16/relatorio.md` nem abriu
issue com a etiqueta `verificacao-mensal`. A pasta `verificacao/` tem apenas `2026-10-01` e
`2026-10-02`, e as duas issues com essa etiqueta são de 2026-09-16 e 2026-10-01. Esta
verificação foi feita de raiz, sem o relatório automático. Vale a pena olhar para o workflow.

## Taxa de referência

Taxa de facilidade de depósito do BCE: **2,50%, inalterada desde 16 de setembro de 2026**
(quadro das taxas diretoras do BCE, lido a 2026-10-16). O ficheiro foi verificado a
2026-10-09, posterior à última subida, por isso nada do que se segue é movimento do BCE.
São repricings dos próprios bancos, e esta quinzena foram quase todos para cima.

## Mudou

- **Haitong Bank, HB Sem Mobilização**: sobe em todos os prazos. 3 meses 2,65% para **2,85%**,
  6 meses 2,70% para **2,85%**, 12 meses 2,75% para **2,95%**, 24 meses 2,75% para **3,05%**
  (site do Haitong Bank, 2026-10-16)
- **Haitong Bank, HB Com Mobilização**: também sobe em todos os prazos. 3 meses 2,60% para
  **2,80%**, 6 meses 2,65% para **2,80%**, 12 meses 2,70% para **2,90%**, 24 meses 2,70% para
  **3,00%** (site do Haitong Bank, 2026-10-16)
- **Banco Finantia, DP Jump**: 6 meses 2,70% para **3,00%**, 12 meses 3,00% para **3,10%**
  (site do Banco Finantia, 2026-10-16)
- **Banco Finantia, DP Visão**: 24 meses 2,90% para **3,15%**, nas duas variantes, mobilização
  antecipada e mobilização semestral (site do Banco Finantia, 2026-10-16)
- **Banco Finantia, Depósito Não Mobilizável**: 6 meses 2,55% para **2,80%**, 12 meses 2,80%
  para **2,90%**, 24 meses 2,75% para **2,95%** (site do Banco Finantia, 2026-10-16)
- **Banco Finantia, Depósito Mobilizável**: 6 meses 2,30% para **2,55%**, 12 meses 2,55% para
  **2,65%**, 24 meses 2,60% para **2,70%** (site do Banco Finantia, 2026-10-16)
- **Banco Montepio, Depósito 6 Meses Novos Capitais**: 2,50% para **2,700%**. Resolve o ponto
  que ficou por confirmar a 2026-10-02: o produto existe e tem taxa publicada na tabela
  (site do Banco Montepio, 2026-10-16)
- **Banco Montepio, Depósito TOP 3 Meses**: 1,25% para **2,250%** (site do Banco Montepio, 2026-10-16)
- **Banco Montepio, Depósito TOP 6 Meses**: 2,15% para **2,500%** (site do Banco Montepio, 2026-10-16)
- **Banco Montepio, Depósito TOP 12 Meses**: 2,25% para **2,500%** (site do Banco Montepio, 2026-10-16)
- **Banco Montepio, Depósito Super 2 Anos**: 2,00% para **2,200%** (site do Banco Montepio, 2026-10-16)
- **Banco Montepio, Depósito TOP Jovem**: 2,15% para **2,250%**, mínimo 25€ e máximo 10.000€
  (site do Banco Montepio, 2026-10-16)
- **Banco Montepio, Poupança com Reforço**: o 1.º ano mantém **1,400%**, que é o que temos, mas
  a página publica também **1,600%** no 2.º ano, que não está na ficha
  (site do Banco Montepio, 2026-10-16)
- **ABANCA, Depósito a Prazo JÁ Livre a 12 meses**: 1,50% para **1,750%**. Além disso o produto
  está agora dividido em duas páginas separadas, DP JÁ 6M Livre e DP JÁ 12M Livre, o que resolve
  a dúvida de 2026-10-02 sobre o prazo de 12 meses não aparecer em lado nenhum. Os 6 meses
  mantêm 1,550%, mínimo 500€, sem máximo (abanca.pt/pt/poupancas/deposito-a-prazo-ja/ e
  .../deposito-a-prazo-ja-6-meses/, 2026-10-16)

### Restrição de idade que ficou por registar

- **Banco Montepio, Depósito TOP Jovem**: a página descreve-o como "Poupança para jovens dos
  0 aos 30 anos". Pela regra de inclusão a entrada devia ter `idade_max: 30` e a etiqueta
  "Até 30 anos". É o ponto que ficou em aberto a 2026-10-02
  (site do Banco Montepio, 2026-10-16)
- **Banco Carregosa, NextGen Welcome Boost**: continua sem `idade_max`. O limite de 30 anos
  foi lido a 2026-10-02 na Mod0739V01_BC_PT_09-26 e não voltou a ser confirmado hoje, porque
  as páginas portuguesas do Carregosa não abrem

## Confirmado sem alteração

Banco BiG Super Depósito (3 meses 4,00% e 6 meses 3,50%, códigos PTDP2026040 e PTDP2026041),
Bison Bank DP Bison Rendimento Premium (3,00% nos quatro prazos, 5.000€ a 250.000€),
Openbank DP Novos Clientes Tri (3 meses 2,30%, 6 meses 2,50%, 12 meses 2,30%),
Bankinter Depósito Net Boas Vindas (6 meses 3,00%, 1.000€ a 100.000€),
BAI Europa Não Mobilizável (3 meses 2,60%, 6 meses 3,05%, 12 meses 3,05%),
BNI Europa Não Mobilizável (6 meses 2,50%, 12 meses 2,55%, 24 meses 2,75%),
ABANCA DP Grow (TANB média 1,1250%, escadaria 0,5000% / 0,7500% / 1,5000% / 1,7500%),
ABANCA DP Poupança (12 meses 1,0000%, mínimo 500€).
Todos lidos hoje nos sites dos próprios bancos.

Sobre o **ABANCA DP Poupança**: a página de produto publica "Montante Mínimo - 500€", enquanto
o ficheiro tem 50€, alterado a partir da FIN a 2026-10-02. A página e a FIN discordam. Vale
confirmar qual manda antes de deixar os 50€.

Sobre o **BAI Europa Não Mobilizável**: o prazo de 24 meses não consta da página. O ficheiro
também não o tem, por isso não há divergência, mas fica o registo.

## Novo

Candidatos com TANB igual ou superior a 1,00%, em euros, em prazos de 3, 6, 12 ou 24 meses,
subscritíveis por qualquer particular. Todos lidos na página do próprio banco a 2026-10-16.

**Banco CTT, Super DP** (bancoctt.pt/as-suas-poupancas/super-dp)

- 6 meses 1,60%, 12 meses 1,75%, 24 meses 1,80%. De 1.000€ a 100.000€. Mobilização antecipada
  total ou parcial com penalização total dos juros sobre o montante mobilizado

**ABANCA, Depósito a Prazo Especial** (abanca.pt/pt/poupancas/deposito-prazo-especial/)

- 12 meses 2,75%, de 15.000€ a 100.000€. Exclusivo a Novos Recursos ABANCA, com saldo global
  superior ao dos 60 dias anteriores. **Só se subscreve em agência**, não há canal digital.
  Mobilização parcial ou total a qualquer momento com penalização total dos juros do montante
  mobilizado. Fica ao teu critério se a subscrição só em balcão desqualifica a entrada

**Santander Totta** (santander.pt/poupancas)

- Depósito Poupança Plus: 3, 6 e 12 meses a 1,30%, de 100.000€ a 300.000€
- Depósito Poupança: 3, 6 e 12 meses a 1,05%, de 15.000€ a 300.000€
- Depósito Aforrador: 6 meses a 1,00%, de 50€ a 15.000€, para quem tem até 30.000€ no Santander

**Millennium BCP, Depósito App** (millenniumbcp.pt/poupanca/comparar)

- 90, 180 ou 360 dias, de 500€ a 500.000€, com taxa por escalão de montante.
  500€ a 49.999,99€: 1,50% em todos os prazos.
  50.000€ a 99.999,99€: 2,00% em todos os prazos.
  100.000€ a 249.999,99€: 2,15% a 90 dias, 2,25% a 180 dias, 2,35% a 360 dias.
  250.000€ a 500.000€: 2,25% a 90 dias, 2,35% a 180 dias, 2,50% a 360 dias

**Crédito Agrícola, DP Net Super** (creditoagricola.pt/particulares/poupar/dp-net-super)

- 92 dias a 1,750%, de 500€ a 15.000€. Só subscritível nos 3 meses seguintes à adesão ao
  homebanking ou à app, é uma oferta de boas-vindas. A página rotula o valor como "Taxa de juro
  fixa", não literalmente TANB, e 92 dias não é exatamente a grelha dos 3 meses. Fica ao teu
  critério

**Caixa Geral de Depósitos**, continuam de fora da lista e continuam a qualificar
(cgd.pt, página de Depósitos a Prazo e Contas Poupança)

- Depósito App 3 Meses: 3 meses 2,00%, de 250€ a 15.000€, subscrição exclusiva na app Caixadirecta
- Depósito Caixa 3 Meses: 3 meses 1,70%, mínimo 250€
- Depósito Caixa Especial 12 Meses: 12 meses 1,65% na taxa base. Sobe a 1,90% com cartão de
  crédito ou domiciliação de rendimento, por isso usa-se a base

Estes três já tinham aparecido no relatório de 2026-10-02 e não entraram no ficheiro.

### Ficaram de fora e porquê

- **ABANCA Depósito a Prazo Cresce**, 2,75%: exige domiciliação de ordenado, pensão ou Segurança
  Social mais um débito direto
- **Santander Depósito Jovem** 1,60% (até 25 anos), **ABANCA Depósito a Prazo Kids** 1,50%,
  **Millennium Poupança Let's GO!**, **CGD Poupança Caixa Júnior** e **Conta Objetivo Jovem**:
  restrição de idade ou destinados a menores
- **Montepio Poupança Super** (3 anos), **Poupança Cresce 3 Anos** (3 anos), **Poupança M24**
  (30 a 180 dias), **Poupança Mealheiro** (30 a 360 dias), **Poupança Especial Jovem**
  (1 ano e 1 dia), **Millennium Poupança Ordenado** e **Poupança Reforço Prestige** (30 dias):
  fora da grelha de 3, 6, 12 e 24 meses
- **Santander Conta Poupança Select +** 0,40%, **Conta Poupança Objetivo** 0,15%,
  **Millennium Net Millennium Flexível** 0,65% a 0,90%: abaixo de 1,00%
- **Depósitos em moeda estrangeira** da CGD, do Santander e do Banco Carregosa: não são em euros

## Desapareceu

Nada. Nenhuma entrada do ficheiro deixou de constar da fonte do próprio banco nesta ronda.

## Links

- **Banco Carregosa**: o endereço guardado `bancocarregosa.com/pt/particulares/poupanca/depositos-a-prazo`
  continua a devolver 404, como a 2026-10-02. A estrutura nova é
  `/solucoes-de-poupanca-e-investimento/depositos-a-prazo/`, mas todas as variantes portuguesas
  que tentei hoje deram erro de cliente. Só a versão inglesa abre. São oito entradas do ficheiro
  sem fonte viva em português
- **Dezasseis entradas continuam com o campo `url_fin` preenchido com o nome do documento em
  vez do endereço**, o que faz o Action falhar sempre nessas linhas: carregosa-bemvindo,
  bai-novos, bai-premium, bai-eur, invest-choice, invest-dp, carregosa-dp, bpi-novos,
  cgd-mais-valor, cgd-novos-recursos, montepio-6m-novos-capitais, montepio-top-6m,
  montepio-top-3m, carregosa-poupanca-crescente, carregosa-rendimento-mensal e
  carregosa-christmas-greetings. Outras **dezanove entradas não têm `url_fin` nenhum**
- **cgd-mais-valor** e **cgd-novos-recursos** continuam a apontar para a página
  `/Depositos-a-Prazo/Pages/Depositos-a-Prazo.aspx`, que não existe. A página viva é
  `/Depositos-a-Prazo-e-Poupanca/Pages/Depositos-a-Prazo-e-Contas-Poupanca.aspx`, já usada
  pelas outras quatro entradas da CGD
- **As sete entradas do Banco Montepio** já apontam para a versão portuguesa,
  `/particulares/poupanca-e-reforma/depositos-prazo`. O ponto levantado a 2026-10-02 está
  resolvido

## Não consegui confirmar

- **Banco Best, Depósito Novos Clientes 6 meses 3,30% e Depósito Novos Recursos 12 meses 2,85%**:
  as duas FIN em PDF devolvem ROBOTS_DISALLOWED e as páginas alternativas do site
  (`/pt/depositos-a-prazo`, `/bestsite/public/poupanca/depositos`,
  `/particulares/poupanca/depositos-a-prazo`) devolvem 404. Nenhuma das duas entradas foi
  verificada nesta ronda. Nota: a 2026-10-02 o produto tinha mudado de nome para "Depósito Novos
  Clientes Aniversário" com taxa de 2,80% a 90 dias, e o ficheiro tem hoje 3,30% a 6 meses.
  Vale um clique
- **Atlântico Europa, DP Global Living, 6 meses 2,50%**: `atlantico.eu` continua a devolver só
  o cabeçalho e `phi_loading.gif`. Casca que exige JavaScript, tal como a 2026-10-02
- **Banco Invest, Invest Depósito a Prazo, 6 meses 2,10%, 12 meses 2,25% e 24 meses 2,25%**:
  a página de aplicações a prazo abre mas as taxas são placeholders de template por preencher,
  literalmente `${singleRate}` e `${penaltyInterest}`. `my.bancoinvest.pt` devolve 302 para a
  homepage, não é fonte separada. Confirmado na página: mínimo de 2.000€ e máximo entre 150.000€
  e 500.000€. O Invest Choice Novos Montantes aparece na homepage a 2,75% com os prazos
  "3 | 6 | 12 meses" numa linha só, sem separação por prazo, e com máximo de 150.000€
- **Klarna, conta poupança a prazo fixo, as oito taxas**: `klarna.com/pt/conta-poupanca/`
  devolve ROBOTS_DISALLOWED, tal como a 2026-10-02. Terceira ronda seguida sem verificação
- **ActivoBank, Depósito Novos Clientes AB**: a TANB de 3,00% a 90 dias está confirmada e o
  cartão tem botão "Constituir", mas a frase "Oferta não disponível" continua a aparecer logo
  a seguir ao cartão, sem estar inequivocamente ligada ao produto no HTML. Ambíguo, precisa de
  olho humano no browser
- **Banco Carregosa, DP Bem-Vindo**: a página portuguesa não abre. A inglesa diz 3 meses 2,50%
  e 6 meses 1,75%, de 25.000€ a 100.000€, e o ficheiro tem 3 meses 3,00% e 6 meses 2,80% com
  mínimo de 5.000€. Mas a página inglesa escreve "APR rate", não TANB, por isso **não dá para
  usar estes números**. É uma divergência grande e precisa da página portuguesa
- **Banco Carregosa, as outras sete entradas**: sem fonte viva nesta ronda, pelo mesmo motivo
- **Novo Banco**: as páginas de campanha devolvem ROBOTS_DISALLOWED e as de produto abrem sem
  uma única taxa. Nada confirmado, em nenhum sentido
- **Crédito Agrícola, todos os DP exceto o DP Net Super**: listados sem taxa, o simulador vem
  por renderizar
- **BPI, DP BPI +**: a página remete a TANB para a FIN e não a publica
- **ABANCA, as FIN em PDF**: DP Grow e DP JÁ devolvem ROBOTS_DISALLOWED. Contornado pelas
  páginas de produto do próprio banco, que são igualmente fonte primária
- **Economia e Finanças** e **Fórum do Investidor**: não tentados nesta ronda. São fontes de
  pistas, nunca de confirmação, por isso não bloqueiam nada

## Nota sobre o TAREFA.md

Continua por corrigir. O `verificacao/TAREFA.md` diz duas vezes que o limiar de inclusão é
TANB igual ou superior a 2,00%, enquanto `meta.regra_inclusao` do `depositos.json` e a instrução
desta verificação dizem 1,00%. Seguiu-se 1,00%, como em 2026-10-02.

## Próximo passo

Rever este relatório. Só depois do teu ok é que se edita `data/depositos.json`, incluindo
`meta.data_verificacao`, e se atualiza a data de verificação na página do comparador e no artigo
dos melhores depósitos a prazo.
