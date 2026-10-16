# Verificação dos depósitos a prazo - 2026-10-16

Verificação quinzenal do dia 16. Base: `data/depositos.json` verificado a 2026-10-09, 58 entradas.

**Nada foi alterado em `data/depositos.json`.** Nem no Webflow, nem na data de verificação.
Este ficheiro é só o relatório. (O `verificacao/TAREFA.md` foi corrigido à parte, ver o fim.)

Cinco bancos que a sessão automática não conseguiu ler foram resolvidos com capturas de ecrã e
com links diretos do Franklin, a 2026-10-16: Klarna, ActivoBank, Trade Republic, Banco Best e
Banco Invest. Estão marcados abaixo. **As quatro entradas em que eu tinha menos confiança,
as duas do Best e as duas do Invest, estavam todas certas.**

## Nota sobre o GitHub Action

O Action das 07:00 UTC de hoje não produziu `verificacao/2026-10-16/relatorio.md` nem abriu
issue com a etiqueta `verificacao-mensal`. A pasta `verificacao/` tinha apenas `2026-10-01` e
`2026-10-02`, e as duas issues com essa etiqueta são de 2026-09-16 e 2026-10-01. Confirmado
duas vezes. Esta verificação foi feita de raiz, sem o relatório automático. Vale a pena olhar
para o workflow.

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
- **Banco Montepio, Depósito 6 Meses Novos Capitais**: 2,50% para **2,700%** (site do Banco
  Montepio, 2026-10-16)
- **Banco Montepio, Depósito TOP 3 Meses**: 1,25% para **2,250%** (site do Banco Montepio, 2026-10-16)
- **Banco Montepio, Depósito TOP 6 Meses**: 2,15% para **2,500%** (site do Banco Montepio, 2026-10-16)
- **Banco Montepio, Depósito TOP 12 Meses**: 2,25% para **2,500%** (site do Banco Montepio, 2026-10-16)
- **Banco Montepio, Depósito Super 2 Anos**: 2,00% para **2,200%** (site do Banco Montepio, 2026-10-16)
- **Banco Montepio, Depósito TOP Jovem**: 2,15% para **2,250%**, mínimo 25€ e máximo 10.000€
  (site do Banco Montepio, 2026-10-16)
- **Banco Montepio, Poupança com Reforço**: o 1.º ano mantém **1,400%**, que é o que temos, mas
  a página publica também **1,600%** no 2.º ano, que não está na ficha
  (site do Banco Montepio, 2026-10-16)
- **ABANCA, Depósito a Prazo JÁ Livre a 12 meses**: 1,50% para **1,750%**. O produto está agora
  dividido em duas páginas, DP JÁ 6M Livre e DP JÁ 12M Livre, o que resolve a dúvida de
  2026-10-02 sobre o prazo de 12 meses. Os 6 meses mantêm 1,550%, mínimo 500€, sem máximo
  (abanca.pt/pt/poupancas/deposito-a-prazo-ja/ e .../deposito-a-prazo-ja-6-meses/, 2026-10-16)
- **Klarna, conta poupança a prazo fixo**, confirmado por captura: duas das quatro taxas da
  nossa grelha mudaram. 3 meses mantém **1,84%**, **6 meses 2,59% para 2,15%**, **12 meses
  3,00% para 2,95%**, 24 meses mantém **3,15%**. O corte a 6 meses é de 44 pontos base.
  A tabela publica ainda 9 meses 2,46%, 18 meses 3,11%, 36 meses 3,19% e 48 meses 3,24%,
  fora da nossa grelha (klarna.com/pt/conta-poupanca/, 2026-10-16)

### Restrição de idade que ficou por registar

- **Banco Montepio, Depósito TOP Jovem**: a página descreve-o como "Poupança para jovens dos
  0 aos 30 anos". Pela regra de inclusão a entrada devia ter `idade_max: 30` e a etiqueta
  "Até 30 anos" (site do Banco Montepio, 2026-10-16)
- **Banco Carregosa, NextGen Welcome Boost**: continua sem `idade_max`. O limite de 30 anos
  foi lido a 2026-10-02 na Mod0739V01_BC_PT_09-26 e não voltou a ser confirmado hoje

## Confirmado sem alteração

### Banco Best, as duas entradas, lidas na FIN

- **Depósito Novos Clientes**, FIN "Depósito Novos Clientes 3,30%": "TANB (Taxa Anual Nominal
  Bruta): 3,30%", "Prazo 180 dias", "Mínimo de constituição: 500€", "Máximo de constituição:
  250.000€", "São permitidas mobilizações antecipadas a qualquer momento, parciais ou totais,
  com penalização total de juros", "Renovação Não aplicável". **Bate certo com a ficha, campo
  a campo**, incluindo o máximo de 250.000€ e o não renovável
  (bancobest.pt/ptg/bestsite/best_docs/FIN_NovosClientes.pdf, 2026-10-16)
- **Depósito Novos Recursos**, confirmado na página de depósitos: "Taxa: 2,85% TANB", "Prazo:
  365 Dias", "Montante Min: 500€", "Renovação automática: Uma vez por igual período à taxa de
  0,10% (TANB)", "Exclusivo para novos recursos!", mobilização antecipada com penalização total
  de juros não pagos. Bate certo com a ficha, incluindo a renovação única a 0,10%. O único
  campo que não vi na fonte é o máximo de 500.000€ que temos guardado, porque a FIN deste
  produto continua bloqueada (bancobest.pt/ptg/depositos, 2026-10-16)

A entrada `best-novos` dizia na nota que "a campanha anterior (2,80% a 90 dias, máx. 75.000€)
terminou". Confirma-se: a campanha a 180 dias e 250.000€ é a que está no ar.

### Banco Invest, as duas entradas, lidas nas FIN

- **Invest Choice Novos Montantes**, FIN de 25 de setembro de 2026: TANB **2,750%** única para
  os três prazos, "Montante mínimo Eur 2 000", "Montante máximo Eur 150 000", "Exclusivo para
  novos montantes no Banco Invest a partir de 17 de Setembro de 2026", "Mobilizações totais ou
  parciais possíveis, mas com penalização de 100% dos juros". **Bate certo com a ficha.** A FIN
  confirma também a leitura de que os 2,75% valem igual a 3, 6 e 12 meses, e não por prazo
  (bancoinvest.pt/docs/default-source/aplicacoesprazo/invest_choice_novos_montantes_20260925.pdf)
- **Invest Depósito a Prazo**, FIN de 17 de setembro de 2026, com a tabela completa:

  | Prazo | desde 2.000€ | desde 50.000€ |
  |---|---|---|
  | 3 meses (92 dias) | 1,900% | 2,000% |
  | 6 meses (183 dias) | 2,100% | 2,200% |
  | 12 meses (365 dias) | 2,250% | 2,350% |
  | 24 meses (730 dias) | 2,250% | 2,350% |

  "Montante mínimo Eur 2 000", "Montante máximo Eur 5 000 000", mobilização com penalização de
  100% dos juros. **Bate certo com a ficha**, e também com a nota que lá está, que já descrevia
  os 1,90% a 3 meses e o escalão dos 50.000€ a mais 0,10 pontos. A ficha tem 6, 12 e 24 meses;
  os 3 meses a 1,90% continuam só na nota e não como prazo
  (bancoinvest.pt/docs/default-source/aplicacoesprazo/invest_deposito_a_prazo_20260917.pdf)

### ActivoBank, confirmado por captura

**Continua disponível**, com botão "Constituir" ativo. TANB 3,00%, prazo 90 dias, de 500€ a
50.000€, para clientes com abertura de conta nos 90 dias anteriores, renovação automática à
taxa do Depósito Standard e mobilização parcial ou total com 100% de penalização dos juros.
**Bate certo com a ficha, campo a campo.** O "Oferta não disponível" que apareceu nas leituras
automáticas de 2026-10-02 e de hoje era de outro cartão da página. Fica encerrado.

### Os restantes

Banco BiG Super Depósito (3 meses 4,00% e 6 meses 3,50%), Bison Bank DP Bison Rendimento
Premium (3,00% nos quatro prazos, 5.000€ a 250.000€), Openbank DP Novos Clientes Tri (2,30% /
2,50% / 2,30%), Bankinter Depósito Net Boas Vindas (6 meses 3,00%), BAI Europa Não Mobilizável
(2,60% / 3,05% / 3,05%), BNI Europa Não Mobilizável (2,50% / 2,55% / 2,75%), ABANCA DP Grow
(TANB média 1,1250%), ABANCA DP Poupança (12 meses 1,0000%).

Sobre o **ABANCA DP Poupança**: a página de produto publica "Montante Mínimo - 500€", enquanto
o ficheiro tem 50€, alterado a partir da FIN a 2026-10-02. A página e a FIN discordam. Vale
confirmar qual manda antes de deixar os 50€.

## Novo

Candidatos com TANB igual ou superior a 1,00%, em euros, em prazos de 3, 6, 12 ou 24 meses,
subscritíveis por qualquer particular. Todos lidos na página ou na FIN do próprio banco a
2026-10-16.

**Banco Best** (bancobest.pt/ptg/depositos) — sete produtos que não temos

- Depósito Especial 6M: 6 meses **1,55%**, mínimo 10.000€
- Depósito Especial 12M: 12 meses **1,65%**, mínimo 10.000€
- Depósito Exclusivo Best App: 3 meses (90 dias) **1,50%**, mínimo 500€
- Conta Poupança Crescente: 6 meses **1,40%** mais prémio de permanência a partir do 2.º
  semestre, renovação automática até 4 semestres, de 125€ a 100.000€. A TANB de 1,40% é a
  base; o prémio não está quantificado na página
- Depósito a Prazo Fixo: 7, 15, 30, 60, 90, 180 ou 365 dias, **entre 1,00% e 1,25%**, mínimo
  500€. Cobre 3, 6 e 12 meses da nossa grelha, mas a página não diz que taxa corresponde a que
  prazo, só o intervalo
- Depósito a Prazo à Medida: 5 a 365 dias, **entre 1,00% e 1,25%**, mínimo 500€. Mesmo problema
  do intervalo
- Depósito Step Up VII: taxas semestrais crescentes de 1,40%, 1,65% e 3,25%, **TANB média
  2,10%**, 18 meses (540 dias), mínimo 10.000€. **Fica de fora pela grelha**, 18 meses não é
  3, 6, 12 nem 24, mas registo-o porque a TANB média é das mais altas do Best

**Banco Invest** (FIN de 17 de setembro de 2026)

- Invest Mais: 6 meses (180 dias) **2,300%**, de 2.000€ a 300.000€. **Tem uma condição que
  precisa da tua decisão**: "Exclusivo para Clientes que detenham mais de 30% em Activos do
  total do seu património na respectiva conta junto do Banco Invest". Não é domiciliação de
  ordenado, que é o que a regra exclui, mas também não é subscritível por qualquer particular
  sem mais nada. Fica ao teu critério
  (bancoinvest.pt/docs/default-source/aplicacoesprazo/invest-mais_20260917.pdf)

**Banco CTT, Super DP** (bancoctt.pt/as-suas-poupancas/super-dp)

- 6 meses 1,60%, 12 meses 1,75%, 24 meses 1,80%. De 1.000€ a 100.000€

**ABANCA, Depósito a Prazo Especial** (abanca.pt/pt/poupancas/deposito-prazo-especial/)

- 12 meses 2,75%, de 15.000€ a 100.000€. Exclusivo a Novos Recursos ABANCA. **Só se subscreve
  em agência**, não há canal digital. Fica ao teu critério

**Santander Totta** (santander.pt/poupancas)

- Depósito Poupança Plus: 3, 6 e 12 meses a 1,30%, de 100.000€ a 300.000€
- Depósito Poupança: 3, 6 e 12 meses a 1,05%, de 15.000€ a 300.000€
- Depósito Aforrador: 6 meses a 1,00%, de 50€ a 15.000€, para quem tem até 30.000€ no Santander

**Millennium BCP, Depósito App** (millenniumbcp.pt/poupanca/comparar)

- 90, 180 ou 360 dias, de 500€ a 500.000€, com taxa por escalão de montante.
  500€ a 49.999,99€: 1,50% em todos os prazos.
  50.000€ a 99.999,99€: 2,00% em todos os prazos.
  100.000€ a 249.999,99€: 2,15% / 2,25% / 2,35%.
  250.000€ a 500.000€: 2,25% / 2,35% / 2,50%

**Crédito Agrícola, DP Net Super** (creditoagricola.pt/particulares/poupar/dp-net-super)

- 92 dias a 1,750%, de 500€ a 15.000€. Oferta de boas-vindas, só nos 3 meses seguintes à adesão
  ao homebanking. A página diz "Taxa de juro fixa", não TANB. Fica ao teu critério

**Caixa Geral de Depósitos**, já propostos a 2026-10-02 e ainda fora da lista

- Depósito App 3 Meses: 3 meses 2,00%, de 250€ a 15.000€, só na app Caixadirecta
- Depósito Caixa 3 Meses: 3 meses 1,70%, mínimo 250€
- Depósito Caixa Especial 12 Meses: 12 meses 1,65% na taxa base

### Ficaram de fora e porquê

- **ABANCA Depósito a Prazo Cresce** 2,75%: exige domiciliação de ordenado, pensão ou Segurança
  Social mais um débito direto
- **Santander Depósito Jovem** 1,60% (até 25 anos), **ABANCA Depósito a Prazo Kids** 1,50%,
  **Millennium Poupança Let's GO!**, **CGD Poupança Caixa Júnior** e **Conta Objetivo Jovem**:
  restrição de idade ou destinados a menores
- **Best Step Up VII** (18 meses), **Montepio Poupança Super** e **Poupança Cresce 3 Anos**
  (3 anos), **Poupança M24** (30 a 180 dias), **Poupança Mealheiro** (30 a 360 dias),
  **Poupança Especial Jovem** (1 ano e 1 dia), **Millennium Poupança Ordenado** e **Poupança
  Reforço Prestige** (30 dias), **Klarna a 9, 18, 36 e 48 meses**: fora da grelha
- **Santander Conta Poupança Select +** 0,40%, **Conta Poupança Objetivo** 0,15%,
  **Millennium Net Millennium Flexível** 0,65% a 0,90%: abaixo de 1,00%
- **Best Depósito a Prazo Moeda Estrangeira** (até 1,75% em USD e 1,50% em GBP) e os depósitos
  em moeda estrangeira da CGD, do Santander e do Banco Carregosa: não são em euros

## Desapareceu

Nada. Nenhuma entrada do ficheiro deixou de constar da fonte do próprio banco nesta ronda.

## Links

Esta secção melhorou muito com os endereços que o Franklin passou.

- **As FIN do Banco Best estavam com o endereço errado, e não era bloqueio.** Falta-lhes o
  `/ptg/`. O ficheiro tem `bancobest.pt/bestsite/best_docs/FIN_NovosClientes.pdf` e o endereço
  que abre é `bancobest.pt/ptg/bestsite/best_docs/FIN_NovosClientes.pdf`. Corrigir nas duas
  entradas. Nota: o da NovosClientes só abriu com o parâmetro `?cb=` no fim; sem ele e o da
  NovosRecursos com `/ptg/` continuam a devolver ROBOTS_DISALLOWED, por isso o `/ptg/` é
  necessário mas pode não ser suficiente para o robot
- **As duas FIN do Banco Invest existem como link e estão guardadas como nome de documento.**
  Passar `invest-choice` e `invest-dp` a apontar para
  `bancoinvest.pt/docs/default-source/aplicacoesprazo/invest_choice_novos_montantes_20260925.pdf`
  e `bancoinvest.pt/docs/default-source/aplicacoesprazo/invest_deposito_a_prazo_20260917.pdf`.
  **Isto resolve o Banco Invest de vez**: os PDF abrem, têm a tabela toda e não dependem de
  JavaScript, ao contrário da página de produto
- **Banco Carregosa**: o endereço guardado continua a devolver 404. A estrutura nova é
  `/solucoes-de-poupanca-e-investimento/depositos-a-prazo/`, mas as variantes portuguesas deram
  erro de cliente. Só a versão inglesa abre, e escreve "APR" em vez de TANB. São oito entradas
  sem fonte viva em português. É o único banco que fica por resolver. Ver a proposta no fim
- **Dezasseis entradas com `url_fin` preenchido com o nome do documento em vez do endereço**:
  carregosa-bemvindo, bai-novos, bai-premium, bai-eur, invest-choice, invest-dp, carregosa-dp,
  bpi-novos, cgd-mais-valor, cgd-novos-recursos, montepio-6m-novos-capitais, montepio-top-6m,
  montepio-top-3m, carregosa-poupanca-crescente, carregosa-rendimento-mensal e
  carregosa-christmas-greetings. **Duas delas, as do Invest, ficam resolvidas acima.** Outras
  dezanove entradas não têm `url_fin` nenhum
- **cgd-mais-valor** e **cgd-novos-recursos** continuam a apontar para
  `/Depositos-a-Prazo/Pages/Depositos-a-Prazo.aspx`, que não existe. A página viva é
  `/Depositos-a-Prazo-e-Poupanca/Pages/Depositos-a-Prazo-e-Contas-Poupanca.aspx`
- **As sete entradas do Banco Montepio** já apontam para a versão portuguesa. Resolvido
- **klarna-fixo** aponta para o redirecionamento `literaciafinanceira.pt/visita/klarnafixo`.
  A fonte primária, `klarna.com/pt/conta-poupanca/`, não está em `url_fin`, que é `null`

## Não consegui confirmar

Encolheu bastante. Sobram estes.

- **Atlântico Europa, DP Global Living, 6 meses 2,50%**: `atlantico.eu` devolve só o cabeçalho
  e `phi_loading.gif`. Casca que exige JavaScript. Ver a proposta no fim
- **Banco Carregosa, DP Bem-Vindo**: a página portuguesa não abre. A inglesa diz 3 meses 2,50%
  e 6 meses 1,75%, de 25.000€ a 100.000€, e o ficheiro tem 3 meses 3,00% e 6 meses 2,80% com
  mínimo de 5.000€. Mas a inglesa escreve "APR rate", não TANB, por isso **não dá para usar
  estes números**. É uma divergência grande e precisa da página portuguesa
- **Banco Carregosa, as outras sete entradas**: sem fonte viva, pelo mesmo motivo
- **Banco Best, o máximo de 500.000€ do Novos Recursos**: a taxa, o prazo e o mínimo estão
  confirmados na página; o máximo só está na FIN, que continua bloqueada
- **Novo Banco**: páginas de campanha com ROBOTS_DISALLOWED e páginas de produto sem taxas
- **Crédito Agrícola, todos os DP exceto o DP Net Super**: listados sem taxa, simulador por
  renderizar
- **BPI, DP BPI +**: a página remete a TANB para a FIN e não a publica
- **Economia e Finanças** e **Fórum do Investidor**: não tentados. São fontes de pistas

## Propostas para as fontes que ainda falham

**Banco Carregosa**, o único banco por resolver. O caminho mais fiável não é a página de
produto, é o **preçário em PDF**, que o `data/corretoras.json` já usa para a parte de bolsa:
`bancocarregosa.com/pt/repositorio/precarios/precario-de-produtos-financeiros-em-vigor-a-partir-de-1-de-outubro-de-2026.pdf`.
É fonte primária pela nossa regra, tem as taxas por prazo e é um PDF estável. Proposta: passar
as oito entradas do Carregosa a usar o preçário em `url_fin`. Se o PDF também bloquear, a
alternativa é o link direto das FIN, que já temos por nome de documento (Mod0244V01,
Mod0063V01, Mod0706, Mod0581V01, Mod0777V01). O padrão do Banco Invest sugere que esses
documentos existem como URL previsível no repositório do banco.

**Atlântico Europa.** O `url` da entrada já é um PDF direto:
`atlantico.eu/DocsGenerator/Public/DownloadFile?fileName=DPATLM1EUR360.pdf`. É a FIN e não
precisa de JavaScript. Proposta: verificar por esse PDF e pô-lo em `url_fin`. Atenção que o
nome diz `360`, ou seja 360 dias, e a entrada está a 6 meses.

**Lição desta ronda, que vale a pena guardar:** três dos quatro bancos "impossíveis" eram
endereços errados ou nomes de documento em vez de links, não bloqueios reais. Vale mais arranjar
o `url_fin` de cada entrada do que arranjar o robot.

## TAREFA.md, corrigido

A contradição do limiar de inclusão estava assinalada em 2026-10-02 e voltou a estar hoje.
**Ficou corrigida nesta ronda**: `verificacao/TAREFA.md` passa a dizer TANB igual ou superior
a 1,00% nos dois sítios onde dizia 2,00%, alinhado com `meta.regra_inclusao`, e ganha uma linha
a dizer que os dois valores têm de mudar juntos. Corrigiu-se também o caminho do relatório, que
é `verificacao/AAAA-MM-DD/relatorio.md` e não `AAAA-MM`, a frase sobre os grandes bancos (que
hoje têm campanhas acima de 2,00%) e escreveram-se as regras que já se seguiam mas não estavam
no ficheiro: idade máxima entra com etiqueta, domiciliação de ordenado fica de fora, e a grelha
é 3, 6, 12 e 24 meses.

Nenhum dado de depósitos foi tocado nessa alteração.

## Próximo passo

Rever este relatório. Só depois do teu ok é que se edita `data/depositos.json`, incluindo
`meta.data_verificacao`, e se atualiza a data de verificação na página do comparador e no artigo
dos melhores depósitos a prazo.
