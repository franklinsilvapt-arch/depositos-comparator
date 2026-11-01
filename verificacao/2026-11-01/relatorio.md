# Verificação dos depósitos a prazo - 2026-11-01

Segunda passagem, feita depois de o Franklin apontar o FIN novo do Banco CTT e pedir nova tentativa
ao que tinha falhado. Esta versão substitui a primeira. Base: `data/depositos.json` com
`meta.data_verificacao` a 2026-10-16 e 75 entradas. Nada foi alterado em nenhum ficheiro de dados.

Na primeira passagem quase todos os sites de bancos bloquearam. Nesta segunda, com procura dos
endereços atuais e com os preçários em PDF em vez das páginas HTML, abriram a CGD, o Montepio, o
Carregosa, o Best e o BPI. Só o BiG continua fechado.

## Contexto

Taxa de facilidade de depósito do BCE nos 2,50%, inalterada na reunião de 29 de outubro. Sem
movimento de mercado, as mudanças são de campanha.

O GitHub Action `verificar-depositos.yml` não produziu relatório. Está agendado para as 07:00 UTC
de hoje e às 08:45 não havia pasta `verificacao/2026-11-01/`, nem commit novo, nem issue com a
etiqueta `verificacao-mensal`. Vale ver o histórico nos Actions.

## Banco CTT: a FIN confirma o que já temos

O FIN que apontaste (`bancoctt.pt/dA/8a409ea8-.../fin_dp_novos_montantes.pdf`, código BCTTPOU97002)
é do **DP Novos Montantes**, que já está na lista, e bate certo com o que lá está: prazo de 365
dias, **TANB 2,7500%**, mínimo 5.000€, máximo 1.000.000€, mobilização antecipada total ou parcial
com penalização total dos juros corridos, exclusivo a novos recursos entrados nos 30 dias
anteriores, sem reforços. Ou seja, não é produto novo, é a mesma entrada confirmada por fonte
primária, o que é bom: passa a ter FIN em vez de só a página.

Duas coisas do FIN que não temos guardadas:

- **Taxa de renovação de 0,5000%** (TANL 0,3600%). O FIN diz "Na 1ª renovação do prazo contratado e
  nas seguintes renovações, a taxa de remuneração a aplicar é" e imprime 0,5000%. O depósito renova
  automaticamente por períodos iguais, com aviso de 30 dias. Isto é material para o leitor e vale
  uma nota, porque 2,75% no primeiro ano e 0,50% depois é uma história diferente de 2,75% sem mais.
- O FIN **não tem data nem número de versão**, só o código. Por isso não dá para dizer se é novo ou
  se é o mesmo documento de sempre. Se o recebeste agora do banco, a data é a tua.

Sugiro guardar o endereço do FIN no campo `url_fin` do `ctt-novos`, que hoje está vazio.

As páginas `bancoctt.pt/poupanca/depositos-prazo` e `/poupanca` devolvem 200 com 107 caracteres, só
meta-tags, por isso o **Super DP** (6m 1,60%, 12m 1,75%, 24m 1,80%) não foi reconfirmado nesta
passagem.

## Mudou

- **BPI, DP BPI+ está mal etiquetado e com as taxas erradas.** O preçário em vigor a 26-10-2026
  (`bancobpi.pt/contentservice/getContent?documentName=PP_WCS01_UCM01002196`) imprime a escada
  **1,000% / 1,050% / 1,100%** sob **"Depósito a Prazo BPI Renovação"**, que são taxas de renovação.
  O **DP BPI+** aparece com escalões de montante: **1,150% / 1,250% / 1,350%** até 99.999,99€ e
  **1,500% / 1,600% / 1,700%** a partir de 100.000€, mínimo 250€ e máximo 500.000€. Nós temos o DP
  BPI+ a 1,00% / 1,05% / 1,10% e uma nota a dizer que acima de 100.000€ sobe para 1,35% / 1,40% /
  1,45%. Nenhum dos dois conjuntos bate certo. Estamos a publicar o produto abaixo do que o banco
  oferece.
  Ressalva: a correspondência entre cada taxa e cada prazo (90, 180 e 360 dias) não foi confirmada.
  A tabela extrai-se sem cabeçalhos alinhados, a página do produto não imprime taxa e o modelo de
  FIN em `.../fin-dp-bpi-mais` traz "TANB 0,00%". A ordem crescente sugere 90, 180 e 360 dias, mas
  não está legível dessa forma. Precisa de confirmação visual no PDF antes de entrar.

## Novo

Candidatos com TANB igual ou superior a 1% e subscritíveis por particulares:

- **Bison Bank, Depósito a Prazo Bison Growth**, 12 meses, TANB 3,00%, de 25.000€ a 500.000€, só
  novos recursos, mobilização com penalização de 100% dos juros, FGD até 100.000€. Só está
  publicado o prazo de 12 meses (bisonbank.com/pt/depositos-a-prazo, 2026-11-01).
- **Banco Carregosa, DP Win-Win**, 6 meses, TANB 2,50%, de 5.000€ a 100.000€, mobilização permitida
  com penalização de 80% dos juros, não renovável (preçário em vigor a 15-10-2026,
  `bancocarregosa.com/pt/repositorio/precarios/folheto-de-comissoes-e-despesas-e-de-taxas-de-juro.pdf`,
  secção 17.2).
- **Banco Carregosa, DP Soma e Segue**, 3 meses, TANB 2,25%, mínimo 5.000€ e máximo igual ao dobro
  do que foi colocado no Bem-vindo, constituição no site do banco, mobilização com penalização de
  80% dos juros (mesmo preçário). Parece ser o produto de continuidade para quem entrou pelo
  Bem-vindo.
- **Banco Best, Depósito Step Up VII**, 18 meses, taxas por semestre de 1,40%, 1,65% e 3,25%, média
  2,10%, de 10.000€ a 1.000.000€, não renovável, juros semestrais (bancobest.pt/ptg/depositos).
  Os 18 meses estão fora da grelha de 3, 6, 12 e 24, por isso é uma decisão tua se entra e como.
- **Banco Best, Leilões de Depósito a Prazo**, 90 dias, taxa fixa 2,75%, desde 1.000€, máximo
  10.000€ por licitação e 20.000€ por leilão. É um mecanismo de leilão, não um depósito de prateleira,
  por isso também é decisão tua.
- **Banco Montepio, Depósito 3 Meses Novos Capitais**, 3 meses, TANB 1,500%, mínimo 5.000€,
  exclusivo novos capitais (preçário em vigor a 09-10-2026,
  `bancomontepio.pt/content/dam/montepio/pdf/geral/precario/folheto-taxas-juro/clientes-particulares/17-taxas-contas-deposito-particulares.pdf`).

Fora da grelha de prazos, para conheceres: BPI Depósito Especial 3 Anos 2,000% e 5 Anos 2,300%, que
são hoje as taxas mais altas do BPI.

## Decisão de regra que te compete

A CGD publica, em dois produtos que já temos, um **escalão bonificado condicionado a cartão de
crédito ou domiciliação de ordenado**:

- Depósito Caixa Especial 12 Meses: 1,65% base e **1,90%** com cartão de crédito ou ordenado
- DP Caixa 150 Anos 6 meses: 1,60% base e **1,85%** com cartão de crédito ou ordenado

A regra do TAREFA.md diz que depósitos que exigem domiciliação de ordenado ficam de fora. Aqui não
é o depósito que exige, é um escalão, e há uma alternativa que não é o ordenado, o cartão de
crédito. Diz-me se queres a taxa base, as duas, ou a bonificada com nota.

Mesma lógica para três poupanças da CGD que passam o limiar mas não são depósitos a prazo
clássicos: Poupança Caixa Júnior 6m 2,50% no primeiro ano, Conta Poupança Diária 6m 1,50% com plano
de entregas diárias, e Conta Objetivo Jovem 181 dias de 1,000% a 1,500% por escalão, titular único
até 30 anos. A Objetivo Jovem encaixaria no campo `idade_max`, se quiseres.

## Confirmado sem alteração

- **CGD**, as oito taxas que temos, todas iguais: Caixa + Valor 12m 2,50%, Novos Recursos 6m 2,60%,
  App 3 Meses 3m 2,00%, Caixa 3 Meses 3m 1,70%, Especial 12 Meses 12m 1,65%, Caixa 24 Meses 24m
  1,90%, 150 Anos 6m 1,60%, +Aforro 6m 2,15% e 12m 2,25%. O endereço mudou, o atual é
  `cgd.pt/Particulares/Poupanca-Investimento/Depositos-a-Prazo-e-Poupanca/Pages/Depositos-a-Prazo-e-Contas-Poupanca.aspx`,
  o caminho passou de `Depositos-Prazo/` para `Depositos-a-Prazo-e-Poupanca/`. Vale atualizar o
  `url` destas nove entradas.
- **Montepio**, seis das sete: TOP 12 Meses 2,50%, TOP 6 Meses 2,50%, TOP 3 Meses 2,25%, Super 2
  Anos 2,20%, TOP Jovem 2,25%, Poupança com Reforço 12m 1,40%. Detalhe novo, a Poupança com Reforço
  paga **1,600% no segundo ano**.
- **Carregosa**, a campanha de Natal está viva e nas mesmas taxas, 3m 2,50%, 6m 2,75% e 12m 3,00%,
  com mínimo 5.000€, máximo 150.000€, sem mobilização antecipada e só para novos montantes, tudo
  igual ao que temos. Bem-vindo 3m 3,00% e 6m 2,80% e Poupança Crescente 12m 2,45% também
  confirmados.
- **Best**, seis: Novos Clientes 6m 3,30%, Novos Recursos 12m 2,85%, Especial 6M 1,55%, Especial
  12M 1,65%, Exclusivo Best App 3m 1,50%, Conta Poupança Crescente 6m 1,40%. Detalhes novos: o
  Novos Recursos renova uma vez a **0,10%**, e a Conta Poupança Crescente tem prémio de permanência
  de 0,125% por semestre a partir do segundo, até 0,375%.
- **BPI**, DP BPI Novos Clientes 6m 2,50% e Depósito Especial BPI 2 Anos 24m 1,900%.
- **Banco Finantia**, as quatro linhas todas, página atualizada a 2026-10-14.
- **Bison Bank**, DP Bison Rendimento Premium 3,00% a 3, 6, 12 e 24 meses, mínimo 5.000€ e máximo
  250.000€.

## Precisões a fazer

- **Banco Best, a Prazo Fixo e à Medida**: estão agora impressos como intervalo, **entre 1,00% e
  1,25%**, onde temos 1,00% fixo. Vale guardar como intervalo.
- **Bison Bank, Rendimento Premium**: o `url` que temos,
  `bisonbank.com/pt-pt/servicos-de-private-banking/dp-bison-rendimento-premium/`, não responde. O
  que abriu foi `.../depositos-a-prazo-rendimento-premium-bison-bank/`. O site acrescenta uma
  restrição que não temos: conta de um só titular, exclusivo a cidadãos portugueses com Cartão de
  Cidadão válido e residentes no EEE.
- **Banco Finantia, DP Visão**: o site publica duas variantes a 24 meses, ambas a 3,15%, uma com
  Mobilização Antecipada e outra com Mobilização Semestral. Temos uma só linha.

## Em aberto, precisa de confirmação visual

Estes quatro são plausíveis mas não ficaram confirmados, e nenhum deve mudar sem um olhar teu:

1. **Montepio, Depósito 6 Meses Novos Capitais, os nossos 2,70%.** O produto existe e continua
   marcado como exclusivo de novos capitais, com mínimo 5.000€, mas o cartão do site não imprime
   taxa e no PDF do preçário a tabela extrai-se desalinhada, com as percentagens desligadas dos
   nomes. Três leituras com prompts diferentes não resolveram. É a secção 17.2 do PDF.
2. **Carregosa, Rendimento Mensal 24 meses, os nossos 2,20%.** Existe no preçário uma linha "24
   Meses 2,20%", mas pode pertencer ao DP Liquidez, cujo mínimo é 100.000€ e não 25.000€. A nossa
   nota já diz que existe também a 36 meses a 2,20%, o que aumenta a hipótese de confusão. O
   preçário imprime Rendimento Mensal 12M a 2,00% e 36M a 2,20%.
3. **Carregosa, o "Depósito a Prazo" simples, os nossos 3m 1,75% / 6m 1,85% / 12m 1,90% / 24m
   2,10%.** Não aparece no preçário em vigor a 15-10-2026, onde "Depósito a Prazo" surge só como
   cabeçalho de categoria. Pode ter saído de comercialização, mas como é uma ausência num PDF cuja
   extração foi problemática, não a dou por confirmada.
4. **BPI, DP BPI+**, a correspondência entre as seis taxas e os prazos de 90, 180 e 360 dias.

## O que não consegui ler

- **Banco BiG**, tudo. O WAF do banco devolve "This page can't be displayed" a toda a leitura
  automática, em HTML e em PDF. A cópia no Portal do Cliente Bancário
  (`clientebancario.bportugal.pt/sites/default/files/precario/0061_/0061_pre.pdf`) abre mas só tem
  a Parte I, o folheto de comissões, e remete para a Parte II para as taxas de juro.
  **Pista útil**: `big.pt/pdf/BIG018b_precario.pdf` é o preçário completo, com o Folheto de Taxas de
  Juro em vigor a **08-10-2026**. É esse o ficheiro a abrir à mão para fechar o BiG. Nenhuma das
  entradas do BiG foi reconfirmada, incluindo o Super Depósito 3m 4,00%, que é a taxa mais alta da
  lista inteira.
- **Carregosa, o canal NextGen.** O preçário geral não cobre os produtos NextGen, e as páginas HTML
  do banco bloqueiam. As nossas três entradas NextGen (Welcome Boost, Grow On e Christmas
  Greetings) têm FINs próprias, confirmadas por ti a 8 e 9 de outubro com os códigos
  Mod0743, Mod0775 e Mod0777, e vivem em endereços `/nextgen/`. Não as toquei e não há razão para
  pensar que saíram, só não foram reconfirmadas nesta passagem.
- **ActivoBank, BNI Europa, Bankinter, Atlântico Europa, Banco Invest, Haitong, BAI Europa, Klarna,
  bunq, Openbank, ABANCA, BBVA, Santander, Millennium BCP, Crédito Agrícola, Banco Português de
  Gestão, Novo Banco**: sem passagem nesta verificação, por limite de tempo e porque vários já
  tinham bloqueado na primeira ronda. O Millennium bloqueia por robots.txt e é sempre verificação à
  mão.
- **Economia e Finanças** e o **post do JRJordao no Fórum do Investidor**: nenhum lido, o primeiro
  porque o Action não correu, o segundo porque a tabela é imagem e o fórum bloqueia pedidos
  automáticos.

## Documentos que não servem de fonte

Três PDFs desatualizados continuam bem posicionados nas pesquisas e dariam números errados:

- `bancocarregosa.com/pt/repositorio/informacoes-legais/ficha-de-informacao-normalizada-dp-natal-gobulling.pdf`
  é a FIN do DP GoBulling Natal de **2014**, válida de 17 de novembro a 25 de dezembro de 2014, 6
  meses a 2,00%. Aparece no topo das pesquisas por "Carregosa depósito Natal".
- `bancobest.pt/ptg/bestsite/best_docs/PRE_FTJ_17_contas_deposito_particulares.pdf`, em vigor desde
  **06-05-2021**.
- `bancobest.pt/ptg/bestsite/best_docs/PRE-FT-Global.pdf`, em vigor desde **05-05-2023**. Este é o
  que está no campo `src` da entrada do Banco Best no `data/corretoras.json`.
- A fonte fiável do Best é a página viva `bancobest.pt/ptg/depositos`, não os PDFs de preçário.

Também vale saber: quatro páginas de produto da CGD que ainda aparecem nas pesquisas devolvem hoje
o 404 da Caixa (`Deposito-Caixa-Mais-12-Meses.aspx`, `DP-Aforro6MM.aspx`,
`deposito-Caixa-Mais-3meses-2025.aspx`, `deposito-Caixa-6meses-2025.aspx`). O catálogo vivo é o da
página de listagem.

E uma incoerência do próprio Banco Best, a assinalar caso alguém pergunte: a taxa em libras aparece
como 1,60% no cartão de detalhe e "Até 1,50%" no comparador da mesma página.

## Próximo passo

Nada a alterar sem o teu ok. Por ordem: o DP BPI+ mal etiquetado, que é o erro mais visível ao
leitor, os cinco candidatos novos, a correção do `url` das nove entradas da CGD, o `url_fin` e a
nota de renovação do CTT, e a decisão sobre os escalões bonificados da CGD. Os quatro itens em
aberto e o BiG ficam para quando puderes abrir os PDFs à mão.
