# Verificação dos depósitos a prazo - 2026-10-16

Verificação quinzenal do dia 16. Base: `data/depositos.json` verificado a 2026-10-09, 58 entradas.

**Nada foi alterado em `data/depositos.json`.** Nem no Webflow, nem na data de verificação.
Este ficheiro é só o relatório. (O `verificacao/TAREFA.md` foi corrigido à parte, ver o fim.)

Seis bancos que a sessão automática não conseguiu ler foram resolvidos com capturas de ecrã e
links diretos do Franklin, a 2026-10-16: Klarna, ActivoBank, Trade Republic, Banco Best, Banco
Invest e Atlântico Europa. **Todas as entradas desses bancos estavam certas.** O Banco
Carregosa fica resolvido por outra via, pela proveniência dos dados, explicada mais abaixo.

## Decisões do Franklin, 2026-10-16

Registadas aqui para a próxima ronda não voltar a perguntar.

- As linhas de "Mudou" ficam **todas aprovadas**
- Os candidatos novos **entram todos**
- Montepio TOP Jovem leva **`idade_max: 30`**
- ABANCA DP Poupança fica com o mínimo de **50€** (manda a FIN, não a página)
- Os 3 meses a 1,90% do Invest Depósito a Prazo ficam **só como nota**, não como prazo
- **Não se acrescentam códigos promocionais** ao comparador de corretoras
- DEGIRO: **fica como está**
- BluOr e N26 no savings: **ficam como estão**
- Trading 212: **tira-se a frase** dos 2,80% a partir de 1 de novembro, que nenhuma fonte
  suporta

## Nota sobre o GitHub Action

O Action das 07:00 UTC de hoje não produziu `verificacao/2026-10-16/relatorio.md` nem abriu
issue com a etiqueta `verificacao-mensal`. A pasta `verificacao/` tinha apenas `2026-10-01` e
`2026-10-02`, e as duas issues com essa etiqueta são de 2026-09-16 e 2026-10-01. Confirmado
duas vezes. Esta verificação foi feita de raiz. Vale a pena olhar para o workflow.

## Taxa de referência

Taxa de facilidade de depósito do BCE: **2,50%, inalterada desde 16 de setembro de 2026**
(quadro das taxas diretoras do BCE, lido a 2026-10-16). O ficheiro foi verificado a 2026-10-09,
posterior à última subida, por isso nada do que se segue é movimento do BCE. São repricings dos
próprios bancos, e esta quinzena foram quase todos para cima.

## Mudou

- **Haitong Bank, HB Sem Mobilização**: 3 meses 2,65% para **2,85%**, 6 meses 2,70% para
  **2,85%**, 12 meses 2,75% para **2,95%**, 24 meses 2,75% para **3,05%**
  (site do Haitong Bank, 2026-10-16)
- **Haitong Bank, HB Com Mobilização**: 3 meses 2,60% para **2,80%**, 6 meses 2,65% para
  **2,80%**, 12 meses 2,70% para **2,90%**, 24 meses 2,70% para **3,00%**
  (site do Haitong Bank, 2026-10-16)
- **Banco Finantia, DP Jump**: 6 meses 2,70% para **3,00%**, 12 meses 3,00% para **3,10%**
  (site do Banco Finantia, 2026-10-16)
- **Banco Finantia, DP Visão**: 24 meses 2,90% para **3,15%**, nas duas variantes
  (site do Banco Finantia, 2026-10-16)
- **Banco Finantia, Depósito Não Mobilizável**: 6 meses 2,55% para **2,80%**, 12 meses 2,80%
  para **2,90%**, 24 meses 2,75% para **2,95%** (site do Banco Finantia, 2026-10-16)
- **Banco Finantia, Depósito Mobilizável**: 6 meses 2,30% para **2,55%**, 12 meses 2,55% para
  **2,65%**, 24 meses 2,60% para **2,70%** (site do Banco Finantia, 2026-10-16)
- **Banco Montepio, Depósito 6 Meses Novos Capitais**: 2,50% para **2,700%**
  (site do Banco Montepio, 2026-10-16)
- **Banco Montepio, Depósito TOP 3 Meses**: 1,25% para **2,250%** (site do Banco Montepio, 2026-10-16)
- **Banco Montepio, Depósito TOP 6 Meses**: 2,15% para **2,500%** (site do Banco Montepio, 2026-10-16)
- **Banco Montepio, Depósito TOP 12 Meses**: 2,25% para **2,500%** (site do Banco Montepio, 2026-10-16)
- **Banco Montepio, Depósito Super 2 Anos**: 2,00% para **2,200%** (site do Banco Montepio, 2026-10-16)
- **Banco Montepio, Depósito TOP Jovem**: 2,15% para **2,250%**, mínimo 25€ e máximo 10.000€.
  **Leva `idade_max: 30`**, porque a página o descreve como "Poupança para jovens dos 0 aos 30
  anos" (site do Banco Montepio, 2026-10-16)
- **Banco Montepio, Poupança com Reforço**: o 1.º ano mantém **1,400%**, mas a página publica
  também **1,600%** no 2.º ano, que não está na ficha (site do Banco Montepio, 2026-10-16)
- **ABANCA, Depósito a Prazo JÁ Livre a 12 meses**: 1,50% para **1,750%**. O produto está agora
  dividido em duas páginas, DP JÁ 6M Livre e DP JÁ 12M Livre. Os 6 meses mantêm 1,550%
  (abanca.pt/pt/poupancas/deposito-a-prazo-ja/ e .../deposito-a-prazo-ja-6-meses/, 2026-10-16)
- **Klarna, conta poupança a prazo fixo**, confirmado por captura: 3 meses mantém **1,84%**,
  **6 meses 2,59% para 2,15%**, **12 meses 3,00% para 2,95%**, 24 meses mantém **3,15%**.
  O corte a 6 meses é de 44 pontos base. A tabela publica ainda 9 meses 2,46%, 18 meses 3,11%,
  36 meses 3,19% e 48 meses 3,24%, fora da nossa grelha
  (klarna.com/pt/conta-poupanca/, 2026-10-16)

## Confirmado sem alteração

### Banco Best, as duas entradas

- **Depósito Novos Clientes**, na FIN: "TANB 3,30%", "Prazo 180 dias", "Mínimo de constituição:
  500€", "Máximo de constituição: 250.000€", mobilizações antecipadas com penalização total de
  juros, "Renovação Não aplicável". **Bate certo campo a campo**
  (bancobest.pt/ptg/bestsite/best_docs/FIN_NovosClientes.pdf, 2026-10-16)
- **Depósito Novos Recursos**, na página: "Taxa: 2,85% TANB", "Prazo: 365 Dias", "Montante Min:
  500€", "Renovação automática: Uma vez por igual período à taxa de 0,10% (TANB)", "Exclusivo
  para novos recursos!". Bate certo, incluindo a renovação única a 0,10%. O único campo que não
  vi na fonte é o máximo de 500.000€ (bancobest.pt/ptg/depositos, 2026-10-16)

### Banco Invest, as duas entradas

- **Invest Choice Novos Montantes**, FIN de 25 de setembro de 2026: TANB **2,750%** única para
  os três prazos, mínimo 2.000€, máximo 150.000€, exclusivo para novos montantes a partir de
  17 de setembro de 2026, mobilização com penalização de 100% dos juros. **Bate certo**, e
  confirma que os 2,75% valem igual a 3, 6 e 12 meses
- **Invest Depósito a Prazo**, FIN de 17 de setembro de 2026:

  | Prazo | desde 2.000€ | desde 50.000€ |
  |---|---|---|
  | 3 meses (92 dias) | 1,900% | 2,000% |
  | 6 meses (183 dias) | 2,100% | 2,200% |
  | 12 meses (365 dias) | 2,250% | 2,350% |
  | 24 meses (730 dias) | 2,250% | 2,350% |

  Mínimo 2.000€, máximo 5.000.000€. **Bate certo com a ficha e com a nota que lá está.** Por
  decisão do Franklin, os 3 meses a 1,90% continuam só na nota e não entram como prazo

### Atlântico Europa, DP Global Living

Confirmado na FIN, que abre sem JavaScript: **TANB 2,500%** a "6 meses (183 dias)", TANL 1,800%
com retenção de 28%, "Mínimo de constituição/manutenção: 2.500 EUR", "Máximo de constituição:
100.000 EUR", "Exclusivo para novos montantes no Banco Atlântico Europa, S.A., de novos Clientes
ou Clientes atuais, que correspondam a incrementos patrimoniais face à posição de 1 de junho de
2026. Limite de um depósito por cliente", "É permitida a mobilização antecipada, parcial ou
total ... com penalização de 100% do juro", "Não permite renovações". **Bate certo campo a
campo com a ficha**, e o `url_fin` guardado já é este PDF
(atlantico.eu/DocsGenerator/Public/DownloadFile?fileName=DPATLM1EUR360.pdf, 2026-10-16).

O que falhava era o campo `url`, que aponta para `atlantico.eu/particulares/poupanca/prazo-fixo`,
uma casca que só carrega com JavaScript. A FIN sempre esteve bem.

### Banco Carregosa, as oito entradas, resolvido por proveniência

As páginas portuguesas abrem no browser mas são cascas de JavaScript: mesmo com o endereço
certo, o que chega ao leitor automático é só o `<title>` e a descrição. Não consegui ler as
taxas por esta via, e o email de atualização do próprio banco traz as tabelas **como imagens**,
que o conector de Gmail lista mas não descarrega.

**Mas a dúvida fica resolvida à mesma, e a conclusão é que os dados estão certos.** A sequência:

1. A 2026-10-08, às 16:30, a Bárbara Castro Fernandes, do Marketing do Banco Carregosa, enviou
   a "Atualização Depósitos a Prazo | Outubro 2026", a anunciar que o banco "aumentou novamente
   as suas Taxas de Juro e adicionou à sua oferta os Depósitos de Natal 3, 6 e 12 meses"
2. A 2026-10-09, às 10:52, o commit `3e67f07` entrou com a mensagem "Banco Carregosa: FINs de
   outubro confirmadas e NextGen Christmas Greetings"

Ou seja, as entradas do Carregosa que estão no ficheiro foram escritas a partir das FIN de
outubro, no dia seguinte ao anúncio do banco, e incluem exatamente os produtos novos que o
email anuncia (Natal e Christmas Greetings). **A fonte é primária e tem uma semana.**

Isto também resolve a divergência que eu tinha levantado. A página inglesa do Bem-Vindo mostra
3 meses 2,50% e 6 meses 1,75%, de 25.000€ a 100.000€, contra os nossos 3 meses 3,00% e 6 meses
2,80% com mínimo de 5.000€. **Não é a nossa ficha que está errada**: a página inglesa escreve
"APR", que não é TANB, e é anterior à subida de outubro. Fica a recomendação de **não** mexer no
Carregosa com base nessa página.

### Os restantes

Banco BiG Super Depósito (4,00% e 3,50%), Bison Bank (3,00% nos quatro prazos), Openbank
(2,30% / 2,50% / 2,30%), Bankinter Net Boas Vindas (3,00%), BAI Europa Não Mobilizável
(2,60% / 3,05% / 3,05%), BNI Europa Não Mobilizável (2,50% / 2,55% / 2,75%), ABANCA DP Grow
(1,1250%), ABANCA DP Poupança (1,0000%).

**ActivoBank, Depósito Novos Clientes AB**, confirmado por captura: continua disponível, com
botão "Constituir" ativo. TANB 3,00%, 90 dias, de 500€ a 50.000€, renovação à taxa do Depósito
Standard, mobilização com 100% de penalização. Bate certo campo a campo. O "Oferta não
disponível" das leituras automáticas era de outro cartão da página.

**ABANCA DP Poupança**: a página diz 500€ e a FIN diz 50€. Por decisão do Franklin, fica a 50€.

## Novo

Todos aprovados pelo Franklin a 2026-10-16. TANB igual ou superior a 1,00%, em euros, em prazos
de 3, 6, 12 ou 24 meses.

**Banco Best** (bancobest.pt/ptg/depositos)

- Depósito Especial 6M: 6 meses **1,55%**, mínimo 10.000€
- Depósito Especial 12M: 12 meses **1,65%**, mínimo 10.000€
- Depósito Exclusivo Best App: 3 meses (90 dias) **1,50%**, mínimo 500€
- Conta Poupança Crescente: 6 meses **1,40%** mais prémio de permanência a partir do 2.º
  semestre, renovação automática até 4 semestres, de 125€ a 100.000€
- Depósito a Prazo Fixo: 7 a 365 dias, **entre 1,00% e 1,25%**, mínimo 500€. A página dá o
  intervalo, não a taxa por prazo
- Depósito a Prazo à Medida: 5 a 365 dias, **entre 1,00% e 1,25%**, mínimo 500€. Mesmo caso

**Banco Invest** — Invest Mais: 6 meses (180 dias) **2,300%**, de 2.000€ a 300.000€. Exclusivo
a clientes com mais de 30% do património em ativos no banco

**Banco CTT, Super DP** — 6 meses 1,60%, 12 meses 1,75%, 24 meses 1,80%, de 1.000€ a 100.000€

**ABANCA, Depósito a Prazo Especial** — 12 meses 2,75%, de 15.000€ a 100.000€, Novos Recursos,
só em agência

**Santander Totta** — Poupança Plus 1,30% (100.000€ a 300.000€), Poupança 1,05% (15.000€ a
300.000€), Aforrador 6 meses 1,00% (50€ a 15.000€), todos a 3, 6 e 12 meses onde aplicável

**Millennium BCP, Depósito App** — 90, 180 ou 360 dias, de 500€ a 500.000€, por escalão:
1,50% até 49.999,99€; 2,00% até 99.999,99€; 2,15% / 2,25% / 2,35% até 249.999,99€;
2,25% / 2,35% / 2,50% até 500.000€

**Crédito Agrícola, DP Net Super** — 92 dias a 1,750%, de 500€ a 15.000€, oferta de boas-vindas

**Caixa Geral de Depósitos** — Depósito App 3 Meses 2,00% (250€ a 15.000€), Depósito Caixa
3 Meses 1,70% (mínimo 250€), Depósito Caixa Especial 12 Meses 1,65% na taxa base

### Ficaram de fora e porquê

- **ABANCA Depósito a Prazo Cresce** 2,75%: exige domiciliação de ordenado
- **Santander Depósito Jovem** (até 25 anos), **ABANCA Kids**, **Millennium Let's GO!**,
  **CGD Poupança Caixa Júnior** e **Conta Objetivo Jovem**: menores ou restrição de idade
- **Best Step Up VII** (18 meses, TANB média 2,10%), **Montepio Poupança Super** e **Cresce
  3 Anos**, **Poupança M24**, **Poupança Mealheiro**, **Poupança Especial Jovem**,
  **Millennium Poupança Ordenado** e **Reforço Prestige**, **Klarna a 9, 18, 36 e 48 meses**:
  fora da grelha de 3, 6, 12 e 24 meses
- **Santander Select +** 0,40%, **Objetivo** 0,15%, **Net Millennium Flexível** 0,65% a 0,90%:
  abaixo de 1,00%
- **Depósitos em moeda estrangeira** do Best (até 1,75% em USD), da CGD, do Santander e do
  Carregosa: não são em euros

## Desapareceu

Nada.

## Links a corrigir

- **As FIN do Banco Best estavam com o endereço errado, e não era bloqueio.** Falta-lhes o
  `/ptg/`. O ficheiro tem `bancobest.pt/bestsite/best_docs/FIN_NovosClientes.pdf` e o que abre é
  `bancobest.pt/ptg/bestsite/best_docs/FIN_NovosClientes.pdf`. Corrigir nas duas entradas
- **As duas FIN do Banco Invest existem como link e estão guardadas como nome de documento.**
  Passar `invest-choice` e `invest-dp` a apontar para
  `bancoinvest.pt/docs/default-source/aplicacoesprazo/invest_choice_novos_montantes_20260925.pdf`
  e `.../invest_deposito_a_prazo_20260917.pdf`. **Resolve o Banco Invest de vez**
- **Atlântico Europa**: o `url_fin` já está certo. O `url` aponta para a casca de JavaScript.
  Vale a pena trocar o `url` para a FIN também, ou pelo menos saber que é a FIN que manda
- **Banco Carregosa**: as páginas abrem no browser mas não no leitor automático. O `url_fin`
  das cinco entradas que têm nome de documento (Mod0244V01, Mod0063V01, Mod0706, Mod0581V01,
  Mod0777V01) continua por converter em link
- **Catorze entradas com `url_fin` preenchido com o nome do documento**, depois de resolvidas
  as duas do Invest: carregosa-bemvindo, bai-novos, bai-premium, bai-eur, carregosa-dp,
  bpi-novos, cgd-mais-valor, cgd-novos-recursos, montepio-6m-novos-capitais, montepio-top-6m,
  montepio-top-3m, carregosa-poupanca-crescente, carregosa-rendimento-mensal e
  carregosa-christmas-greetings. Outras dezanove não têm `url_fin` nenhum
- **cgd-mais-valor** e **cgd-novos-recursos** apontam para
  `/Depositos-a-Prazo/Pages/Depositos-a-Prazo.aspx`, que não existe. A viva é
  `/Depositos-a-Prazo-e-Poupanca/Pages/Depositos-a-Prazo-e-Contas-Poupanca.aspx`
- **klarna-fixo** tem `url_fin` a `null`. A fonte primária é `klarna.com/pt/conta-poupanca/`
- **As sete entradas do Banco Montepio** já apontam para a versão portuguesa. Resolvido

## Não consegui confirmar

Encolheu para quatro pontos, e nenhum bloqueia a atualização.

- **Banco Best, o máximo de 500.000€ do Novos Recursos**: a taxa, o prazo e o mínimo estão
  confirmados na página; o máximo só está na FIN, que continua com ROBOTS_DISALLOWED mesmo com
  o `/ptg/`
- **Banco Carregosa, as taxas lidas diretamente**: resolvido por proveniência, como acima, mas
  não relido nesta ronda. A próxima verificação devia conseguir ler as FIN se os links forem
  convertidos
- **Novo Banco**: páginas de campanha com ROBOTS_DISALLOWED e páginas de produto sem taxas.
  Nada confirmado, em nenhum sentido
- **Crédito Agrícola, todos os DP exceto o DP Net Super**, e **BPI, DP BPI +**: listados sem
  taxa, ou com a taxa remetida para a FIN

## Lição desta ronda

Dos seis bancos "impossíveis", cinco eram endereços errados, nomes de documento em vez de links,
ou páginas de produto em vez da FIN. Só o Carregosa é que é mesmo uma casca de JavaScript, e
esse resolve-se pela FIN. **Vale mais arranjar o `url_fin` de cada entrada do que arranjar o
robot.** A prioridade para a próxima ronda é converter os catorze `url_fin` que são nomes de
documento em links reais.

## TAREFA.md, corrigido

A contradição do limiar estava assinalada desde 2026-10-02. **Ficou corrigida nesta ronda**:
passa a dizer TANB igual ou superior a 1,00% nos dois sítios onde dizia 2,00%, alinhado com
`meta.regra_inclusao`, com uma linha a dizer que os dois valores mudam juntos. Corrigiu-se
também o caminho do relatório (`AAAA-MM-DD`), a frase sobre os grandes bancos, e escreveram-se
as regras que já se seguiam mas não estavam no ficheiro: idade máxima entra com etiqueta,
domiciliação de ordenado fica de fora, e a grelha é 3, 6, 12 e 24 meses.

## Próximo passo

Com as decisões já tomadas, segue-se a edição de `data/depositos.json` (taxas, candidatos novos,
`idade_max` do TOP Jovem, correções de `url_fin`, `meta.data_verificacao`), a atualização da data
de verificação na página do comparador e a atualização do artigo dos melhores depósitos a prazo.
