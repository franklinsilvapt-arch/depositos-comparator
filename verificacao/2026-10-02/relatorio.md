# Verificação dos depósitos a prazo - 2026-10-02

Verificação quinzenal do dia 1, corrida a 2 de outubro de 2026. Base: `data/depositos.json`
verificado a 2026-09-26, 51 entradas.

Assenta no relatório automático de `verificacao/2026-10-01/relatorio.md` e na issue #2
(etiqueta `verificacao-mensal`), gerados pelo GitHub Action às 07:00 UTC de 2026-10-01. As
páginas guardadas em `verificacao/2026-10-01/paginas/` são leituras dos sites dos próprios
bancos nessa data e foram usadas como fonte primária sempre que a releitura ao vivo falhou.

**Nada foi alterado.** Nem `data/depositos.json`, nem o Webflow, nem a data de verificação.
Este ficheiro é só o relatório.

## Taxa de referência

Taxa de facilidade de depósito do BCE: **2,50% desde 16 de setembro de 2026**, subida de
2,25% (BCE, quadro das taxas diretoras). A última verificação do ficheiro é de 2026-09-26,
posterior à subida, por isso o movimento do BCE já estava refletido à partida. As mudanças
abaixo são repricings dos próprios bancos, em ambos os sentidos.

## Mudou

- **Bison Bank · DP Bison Rendimento Premium**: passa a 3,00% TANB em todos os prazos. 6 meses
  2,00% para 3,00%, 12 meses 2,25% para 3,00%, 24 meses 2,50% para 3,00%, e ganha prazo de
  3 meses a 3,00%. Mínimo desce de 25.000€ para 5.000€ e aparece máximo de 250.000€. Penalização
  de 100% dos juros na mobilização antecipada, mantém-se (site do Bison Bank, 2026-10-02)
- **Banco Finantia · DP Jump**: 6 meses 2,65% para 2,70%, 12 meses 2,80% para 3,00%
  (site do Banco Finantia, 2026-10-02)
- **Banco Finantia · Depósito Mobilizável**: 6 meses 2,25% para 2,30%, 12 meses 2,40% para
  2,55%. 24 meses mantém 2,60% (site do Banco Finantia, 2026-10-02)
- **Banco Finantia · Depósito Não Mobilizável**: 12 meses 2,65% para 2,80%. 6 meses mantém
  2,55% e 24 meses mantém 2,75% (site do Banco Finantia, 2026-10-02)
- **Banco Finantia · DP Visão**: 24 meses mantém 2,90% nas duas variantes, mobilização
  antecipada e mobilização semestral (site do Banco Finantia, 2026-10-02)
- **Banco Finantia, as cinco fichas**: a página passa a publicar máximo de 500.000€ em todos
  os produtos. O campo `max` está a `null` nas cinco entradas (site do Banco Finantia, 2026-10-02)
- **Banco Finantia, nomes**: a página já não usa "DP Jump" nem "DP Visão". As secções chamam-se
  agora "Depósitos em Destaque", "Mobilização Antecipada" e "Mobilização Semestral". Os nomes
  antigos sobrevivem nos nomes dos ficheiros FIN (site do Banco Finantia, 2026-10-02)
- **Banco Português de Gestão · BPG Valor**: corte em toda a linha. 3 meses 2,25% para 1,500%,
  6 meses 2,25% para 1,500%, 12 meses 2,40% para 1,650%. Mínimo e máximo de particulares
  mantêm-se em 5.000€ e 750.000€. A coluna de empresas é mais baixa, 1,250% a 3 e 6 meses e
  1,500% a 12 meses (site do BPG, página guardada a 2026-10-01)
- **ActivoBank · Depósito Dinheiro Novo Plus AB**: 180 dias 2,50% para 2,60%. Mínimo mantém
  50.000€ (site do ActivoBank, 2026-10-02)
- **ActivoBank · Depósito Novos Clientes**: taxa mantém 3,00% a 90 dias e mínimo 500€, mas o
  máximo publicado é 50.000€ e temos 10.000€. O nome passa a "Depósito Novos Clientes AB"
  (site do ActivoBank, 2026-10-02)
- **BPI · Depósito Especial BPI 2 Anos**: 24 meses 1,80% para 1,90%, na FIN do próprio BPI.
  Resolve o `a_confirmar: true` desta entrada. Os 3,10% que o Action apanhou nesta FIN são a
  tranche em USD e os 1,60% a tranche em CAD (FIN do BPI, página guardada a 2026-10-01)
- **ABANCA · DP Poupança**: mínimo 500€ para 50€, segundo a FIN. Taxa mantém 1,0000% a
  12 meses. A FIN está datada de 24-11-2025 (FIN da ABANCA, página guardada a 2026-10-01)
- **Banco Best · Depósito Novos Clientes**: o produto passa a chamar-se "Depósito Novos
  Clientes Aniversário". Taxa 2,80%, prazo 90 dias e montantes de 500€ a 75.000€ mantêm-se
  (site do Banco Best, 2026-10-02)
- **Banco Invest · Choice Novos Montantes**: ganha prazo de 12 meses a 2,75%. A oferta é agora
  2,75% a 3, 6 ou 12 meses, mínimo 2.000€ (my.bancoinvest.pt/novos-montantes, 2026-10-02)
- **Openbank · DP Novos Clientes Tri**: ganha 3 meses a 2,30% e 12 meses a 2,30%. 6 meses
  mantém 2,50%. Mínimo 1€, sem máximo, e 0,20% TANB em caso de mobilização antecipada
  (site do Openbank, 2026-10-02)

### Restrições de idade a registar

- **Banco Carregosa · NextGen Welcome Boost**: taxas confirmadas, 3 meses 3,00% e 6 meses
  2,80%, mínimo 1.000€ e máximo 100.000€, mas o documento diz "exclusivo para clientes do canal
  NextGen, em que todos os titulares tenham idade igual ou inferior a 30 anos". A entrada não
  tem `idade_max`. Pela regra de inclusão devia entrar com a etiqueta "Até 30 anos"
  (Mod0739V01_BC_PT_09-26, 2026-10-02)
- **Banco Montepio · Depósito TOP Jovem**: 6 meses 2,150%, mínimo 25€ e máximo 10.000€,
  confirmado. Falta verificar à mão se tem limite de idade e qual, para preencher `idade_max`
  (site do Banco Montepio, 2026-10-02)

## Novo

Candidatos com TANB igual ou superior a 1,00%, em euros, subscritíveis por qualquer particular.
Todos confirmados na tabela publicada pelo próprio banco.

**Bankinter** (site do Bankinter, 2026-10-02)

- Depósito TOP: 3 meses 2,50% e 6 meses 3,00%, de 5.000€ a 250.000€
- Depósito Digital: 3 meses 2,75%, de 5.000€ a 50.000€
- Depósito TOP Premier: 3 e 6 meses 2,50%, de 250.000€ a 500.000€
- Depósito Net: 7 dias a 12 meses, 0,15% a 2,25% conforme montante e prazo, de 500€ a
  10.000.000€

**Banco Carregosa** (tabela do Banco Carregosa, página guardada a 2026-10-01)

- DP Banco Carregosa Soma e Segue: 3 meses 2,25%, de 5.000€ a 200.000€. Exclusivo de quem
  subscreveu o DP Bem-Vindo
- DP Banco Carregosa Win-Win: 6 meses 2,50%, de 5.000€ a 100.000€
- DP Banco Carregosa Poupança Crescente: 12 meses 2,25%, de 10.000€ a 500.000€, permite reforços
- DP Banco Carregosa Rendimento Mensal 12 Meses: 12 meses 2,00%, de 25.000€ a 1.000.000€
- DP Banco Carregosa Rendimento Mensal 24 Meses: 24 meses 2,20%, de 25.000€ a 1.000.000€

**Caixa Geral de Depósitos** (site da CGD, página guardada a 2026-10-01)

- Depósito App 3 Meses: 3 meses 2,00%, de 250€ a 15.000€, subscrição exclusiva na app Caixadirecta
- Depósito Caixa Especial 12 Meses: 12 meses 1,65% standard, mínimo 500€. Sobe a 1,90% com
  cartão de crédito ou domiciliação de rendimento, por isso a taxa a usar é a standard
- Depósito Caixa 3 Meses: 3 meses 1,70%, mínimo 250€

**ActivoBank** (site do ActivoBank, 2026-10-02)

- Depósito Dinheiro Novo AB: 90 dias 2,25%, mínimo 10.000€
- Depósito Flash: 100 dias, 2,10% de 2.500€ a 19.999€ e 2,50% de 20.000€ a 100.000€
- Depósito Especial Flexível: 100, 180 ou 360 dias, 1,75% a 2,50% conforme montante e prazo,
  mínimo 500€

**Banco BiG** (tabela de depósitos do BiG, 2026-10-02)

- Depósito a Prazo a 3 Meses PTDP2025093: 1,40%, de 1.000€ a 500.000€
- Depósito a Prazo a 6 Meses PTDP2026015: 1,55%, de 1.000€ a 500.000€
- Depósito a Prazo a 1 Ano PTDP2026018: 1,70%, de 1.000€ a 500.000€
- Dep. a Prazo 3 meses TOP PTDP2025094: 1,50%, de 50.000€ a 500.000€
- Dep. a Prazo 6 meses TOP PTDP2026017: 1,65%, de 50.000€ a 500.000€
- Dep. a Prazo 12 meses TOP PTDP2026020: 1,80%, de 50.000€ a 500.000€
- Depósito Renda Mensal 6 meses PTDP2026016: 1,65%, de 10.000€ a 500.000€
- Depósito Renda Mensal 12 meses PTDP2026019: 1,80%, de 10.000€ a 500.000€

**Banco Montepio** (site do Banco Montepio, 2026-10-02)

- Depósito 3 Meses Novos Capitais: 3 meses 1,500%, mínimo 5.000€, exclusivo para novos capitais,
  permite mobilização antecipada

**BNI Europa** (site do BNI Europa, 2026-10-02)

Variantes das fichas que já temos, ficam ao critério do Franklin.

- Não Mobilizável Juros Mensais: 6 meses 2,45%, 12 meses 2,50%, 24 meses 2,70%, mínimo 2.500€
- Mobilizável Não Renovável: 3 meses 2,20%, 6 meses 2,25%, 12 meses 2,30%, 24 meses 2,45%,
  mínimo 2.500€

### Ficaram de fora e porquê

- **ABANCA, depósito a 12 meses com TANB de 2,50%**: exige domiciliação de ordenado, pensão ou
  pagamentos à Segurança Social mais a ativação de um débito direto. A regra de inclusão exclui
  depósitos com restrição de domiciliação de ordenado (catálogo da ABANCA, 2026-10-01)
- **Bankinter Depósito BK Mini, CGD Poupança Caixa Júnior, ABANCA Depósito a Prazo Kids**:
  destinados a menores
- **Depósitos em dólares do BiG e do Banco Carregosa**, incluindo os 4,00% e 3,50% do BiG: não
  são em euros
- **Carregosa Rendimento Mensal 36 Meses 2,20%, ActivoBank Depósito Crescente 3 anos AB 2,42%
  média, CGD Conta Poupança Diária 0,25% standard, Montepio Poupança M24 0,75% e Poupança
  Mealheiro 0,750%**: fora da grelha de 3, 6, 12 e 24 meses ou abaixo de 1,00%

## Desapareceu

- **BPG Valor a 24 meses**: a tabela do BPG passou a mostrar só 3, 6 e 12 meses. Temos 24 meses
  a 2,40% (site do BPG, página guardada a 2026-10-01)

## Links

- **cgd-mais-valor** e **cgd-novos-recursos** apontam para
  `https://www.cgd.pt/Particulares/Poupanca-Investimento/Depositos-a-Prazo/Pages/Depositos-a-Prazo.aspx`,
  que devolve "ESTA PÁGINA NÃO EXISTE". Já estava morto a 2026-10-01. A página viva é
  `https://www.cgd.pt/Particulares/Poupanca-Investimento/Depositos-a-Prazo-e-Poupanca/Pages/Depositos-a-Prazo-e-Contas-Poupanca.aspx`,
  que é a que as outras quatro entradas da CGD já usam
- **As sete entradas do Banco Montepio** apontam para a versão inglesa do site,
  `/en/individuals/savings-and-retirement/term-deposits`. Abre e tem as taxas, mas serve inglês
  a um comparador português
- **Dez entradas têm o campo `url_fin` preenchido com o nome do documento em vez do endereço**,
  o que faz o Action falhar sempre nessas linhas: carregosa-bemvindo, bai-novos, bai-premium,
  bai-eur, invest-choice, invest-dp, carregosa-dp, atlantico-global, bpi-novos, cgd-mais-valor,
  cgd-novos-recursos, montepio-6m-novos-capitais, montepio-top-6m e montepio-top-3m
- **Vinte e uma entradas sem `url_fin`**, como lista a secção 4 do relatório do Action

## Não consegui confirmar

- **Atlântico Europa · DP Global Living**, 6 meses 2,50%: a página de prazo fixo só carrega com
  JavaScript e devolve apenas o cabeçalho, nas duas variantes de endereço. A FIN está guardada
  como nome de documento, não como link
- **Banco Invest · Invest Depósito a Prazo**, 6 meses 2,10%, 12 meses 2,25% e 24 meses 2,25%: a
  tabela de aplicações a prazo é preenchida por JavaScript e serve só variáveis de template. A
  página inicial do banco e o my.bancoinvest.pt só mostram o Choice Novos Montantes. A FIN está
  guardada como nome de documento
- **Klarna · Conta poupança a prazo fixo**, toda a ficha: `klarna.com` está bloqueado por
  robots.txt e o redirecionamento `literaciafinanceira.pt/visita/klarnafixo` também. Nenhuma das
  oito taxas foi verificada nesta ronda
- **ABANCA · DP Grow (crescente)**, 12 meses 1,125%: a FIN é um PDF cifrado que nem o Action nem
  esta sessão conseguiram abrir
- **ABANCA · Depósito a Prazo JÁ Livre a 12 meses**, 1,50%: a página e a FIN cobrem só os 6 meses
  e o produto chama-se "Depósito a Prazo Já 6 Meses Livre". O prazo de 12 meses não aparece em
  nenhuma das duas. Os 6 meses a 1,550% estão confirmados
- **Banco Montepio · Depósito 6 Meses Novos Capitais**, 6 meses 2,50%: o produto continua
  anunciado no banner de topo como novidade, mas já não tem cartão com taxa na página. A leitura
  automática de hoje atribuiu-lhe 1,500%, que é a taxa do cartão do Depósito 3 Meses Novos
  Capitais. Precisa de uma leitura da FIN 150CEUR20260921
- **ActivoBank · Depósito Novos Clientes**: junto ao cartão aparece "Oferta não disponível".
  Pode ser do cartão seguinte. Confirmar se continua subscritível antes de manter os 3,00% em
  destaque
- **Banco Carregosa, página de depósitos a prazo**: devolveu 404 hoje com e sem barra final. Os
  valores da tabela vêm da leitura da própria página pelo Action a 2026-10-01, que é fonte
  primária com nove dias. Vale a pena um clique para confirmar que a página mudou de endereço
- **BBVA · Depósito a Prazo Crescente 1 Ano**: confirmado hoje ao vivo, TANB média 1,163% com
  escadaria de 0,90%, 1,00%, 1,25% e 1,50% por trimestre, de 10.000€ a 500.000€. O Action tinha
  falhado com 403 nas duas fontes
- **Economia e Finanças**: 403. Serve de fonte de pistas, nunca de confirmação, por isso não
  bloqueia nada
- **Fórum do Investidor, post do JRJordao**: a tabela é uma imagem e o fórum bloqueia pedidos
  automáticos. Terceira verificação não feita

## Nota sobre o TAREFA.md

`verificacao/TAREFA.md` diz duas vezes que o limiar de inclusão é TANB igual ou superior a
2,00%. O campo `meta.regra_inclusao` do `depositos.json` e a instrução desta verificação dizem
1,00%, e o ficheiro já tem entradas a 1,00%. Seguiu-se 1,00%. O TAREFA.md precisa de ser
corrigido para não contradizer os dados.

## Próximo passo

Rever este relatório. Só depois do ok do Franklin é que se edita `data/depositos.json`,
incluindo `meta.data_verificacao`, e se atualiza a data de verificação na página do comparador
e no artigo dos melhores depósitos a prazo.
