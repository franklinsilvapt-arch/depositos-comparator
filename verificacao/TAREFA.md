# Tarefa quinzenal: verificar os depósitos a prazo do comparador

Corre nos dias 1 e 16 de cada mês (ou quando o Franklin pedir). O dia 1 apanha o Excel novo do Economia e Finanças; o dia 16 apanha as mudanças de meio de mês nos sites dos bancos. O objetivo é um relatório
curto que o Franklin aprova em 10 minutos. Nunca alterar `data/depositos.json`
sem aprovação explícita.

## Passos

0. Correr `python3 scripts/verificar_precarios.py`, que lê os preçários em PDF declarados
   em `data/precarios.json`. Começar por aqui: os sites dos bancos bloqueiam leitura
   automática (a 1 nov 2026 falharam BiG, Best, Carregosa, BAI, Invest, Haitong, Montepio,
   BPI, Novo Banco e Santander) e os preçários dos mesmos bancos abriram sem problema.
   O preçário é também o documento vinculativo, com data de entrada em vigor impressa.
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
   - escrever os patches da ronda em `verificacao/AAAA-MM-DD/`, um por fonte
     (`alteracoes.json` para as páginas dos bancos, `alteracoes-taxas.json`,
     `alteracoes-fins.json`, `alteracoes-precarios.json`), e por cima deles um
     `ronda.json` com a lista pela ordem de aplicação. Um dispatch do workflow
     `aplicar-alteracoes.yml` com o caminho do `ronda.json` aplica a ronda toda de
     uma vez, tudo ou nada: se um guard do `de` falhar, não fica nada aplicado a
     meio. Nunca reescrever o `data/depositos.json` inteiro à mão,
   - o campo do dispatch é obrigatório. Deixá-lo em branco faz o GitHub recusar a
     execução antes de o workflow arrancar, e não aparece erro nenhum nos logs,
   - a data da página do comparador NÃO se mexe à mão: o `gerar_js.py` injeta o
     `meta.data_verificacao` no chip "Última verificação" e na linha do rodapé, e o
     workflow `gerar-js.yml` dispara sozinho em qualquer push a `data/depositos.json`.
     Basta pôr `data_verificacao` no patch. À mão fica só a data no artigo dos
     melhores depósitos a prazo,
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

- **Nenhuma entrada fica marcada `a_confirmar`, e nenhuma nota fica a dizer "A CONFIRMAR".**
  Se houver alguma coisa que não dê para confirmar com fonte primária, avisar o Franklin
  nomeando o que falta e onde, para ele ir buscar à mão. Só depois é que a alteração entra.
  Deixar um item por confirmar na lista publicada não é opção (regra do Franklin, 2 nov 2026).
- **Avisar o Franklin assim que a verificação estiver feita, antes de aplicar as alterações**,
  para ele aprovar e publicar depressa em vez de o patch ficar à espera. A ronda de
  1 de novembro de 2026 ficou um dia parada num PR e a página continuou a dizer
  "Última verificação 16 de outubro" (regra do Franklin, 2 nov 2026).
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
- A grelha de prazos é 3, 6, 12 e 24 meses. É a grelha do seletor de prazo e é com
  ela que se decide a taxa em destaque e a ordenação do comparador.
- **Prazos acima dos 24 meses entram no JSON e aparecem na tabela "Taxas por prazo" do
  detalhe, mas não no seletor nem na ordenação** (regra do Franklin, 2 nov 2026). Um
  depósito a 12, 24 e 60 meses mostra as três linhas no detalhe, continua a ser comparado
  pela melhor taxa até 2 anos, e o 60 nunca o empurra no ranking.
- **Um depósito cujo único prazo é acima dos 24 meses fica de fora.** Sem nenhum prazo da
  grelha, o cartão não tem taxa nem prazo para pôr em destaque. Foi o caso do Depósito 3
  Anos do Millennium BCP, 1080 dias com TANB média de 2,17% (decisão do Franklin, 2 nov
  2026). O `validar_depositos.py` recusa uma entrada nessas condições.
- Um prazo fora da grelha mas dentro dos 2 anos, como 18 meses, não entra: não tem onde
  aparecer nem no seletor nem como linha coerente com as outras. Se aparecer um produto
  assim que valha a pena, falar com o Franklin antes de mexer na grelha.
- Números em formato pt-PT no relatório (2,75%, 5.000€).
- O preçário de cada banco é UM ficheiro só, com a Parte I (folheto de comissões e
  despesas) e a Parte II (folheto de taxas de juro) dentro do mesmo PDF. No ActivoBank,
  por exemplo, a Parte II começa na página 40 de 62. Não andar à procura de um segundo
  ficheiro para as taxas: a secção 17.2 está lá mais à frente no mesmo documento.
- Ler o preçário com `pdftotext -layout` e não por fetch de página. O fetch devolve só
  os primeiros ~39 mil caracteres em texto verdadeiro e resume o resto, e o resumo
  engana: num preçário cujo índice fica nessas primeiras páginas, o resumo chega a dizer
  que a secção 17.2 não existe quando ela está lá. Além disso o fetch desalinha as
  colunas e deixa de se poder atribuir cada taxa ao prazo e ao escalão certos. É por isto
  que o `verificar_precarios.py` descarrega o PDF e corre o `pdftotext -layout`, e é por
  isto que ele corre na Action e não a partir de uma sessão de chat.
- O portal do Cliente Bancário do Banco de Portugal tem os preçários de todas as
  instituições e o caminho é previsível: `/sites/default/files/precario/<codigo>_/<codigo>_pre.pdf`,
  testado com 0061 (BiG) e 0010 (BPI). As páginas HTML do portal é que não abrem, por isso
  o código de cada instituição tem de vir de outro lado. Vale a pena experimentar este
  caminho no `data/precarios.json` quando o site de um banco não der o PDF.
