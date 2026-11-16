# Cruzamento com o Excel do Economia e Finanças - 2026-11-16

Ficheiro: `Melhores-Taxas-de-Juro-de-Depositos-a-Prazo-Novembro-2026-v4.xlsx`, fornecido pelo Franklin.
Cruzado com as 85 entradas e 165 pares produto-prazo do `data/depositos.json` (verificado a 2026-11-01).

**Aviso que manda em tudo o que vem a seguir:** o Excel apanha mudanças, não as confirma. Nada desta lista entra no
JSON sem o site do banco, a FIN ou o preçário. É uma lista de pistas.

## O que o Excel é, e o que não é

- 311 linhas, 25 bancos, cabeçalho na linha 8, folhas "Todos os depósitos" e "Tabela Dinâmica".
- A coluna "Confirmado em" tem duas datas e mais nenhuma: 2 de novembro de 2026 (54 linhas) e 3 de novembro de 2026
  (257 linhas). **O Excel é contemporâneo da nossa ronda de 1 de novembro, não é mais fresco.** Não vai apanhar nada
  que tenha mexido a meio de novembro, como a subida da Klarna nos prazos curtos que foi confirmada hoje no site.
- O valor do Excel nesta ronda não está em taxas novas. Está em produtos e bancos inteiros que nunca tivemos.
- Não tem nenhuma linha de bonificação DECO ou Proteste, por isso a regra não chegou a ser acionada. A tabela do
  JRJordao tem essas notas no BAI Europa e no Haitong, e foram ignoradas.

## Excluidos pelas regras, antes de comparar

- **Só para menores (1 linha):** Bankinter BK Mini, 1 ano, 5,00%. Já estava fora de propósito.
- **Domiciliação de ordenado (18 linhas):** Bankinter Mais Ordenado 1 ano 5,00%, ABANCA Depósito Cresce 1 ano 2,75%,
  ActivoBank Novo Ordenado AB, Millennium BCP APP em sete prazos e escalões entre 1,50% e 2,50%, Millennium BCP
  Poupança Ordenado e Poupança Reforço. Os dois primeiros são as taxas mais altas do ficheiro inteiro, o que mostra
  que a regra está a fazer trabalho.
- **IGCP (11 linhas):** certificados de aforro e do tesouro, não são depósitos a prazo.

Sobram 292 candidatas com TANB igual ou superior a 1,00%, das quais 241 caem na grelha de 3, 6, 12 e 24 meses.

## 1. Novo Banco: não temos uma única entrada

É o maior buraco. O Excel tem 21 linhas do Novo Banco na grelha com TANB igual ou superior a 1,00% e o nosso ficheiro
não tem o banco de todo. O relatório de 1 de novembro explica porquê: o URL que temos no catálogo devolve 404.

As quatro que interessam:

| TANB | Prazo | Produto | Mínimo | Máximo | Condições |
|---|---|---|---|---|---|
| 3,25% | 6 meses | Novos Clientes | 10.000€ | 500.000€ | Novos clientes e novos capitais, perda total de juros |
| 3,00% | 12 meses | Novos Recursos | 100€ | 5.000€ | Novos capitais |
| 2,75% | 12 meses | Novos Recursos II | 10.000€ | 500.000€ | Dinheiro transferido de outra instituição |
| 2,75% | 24 meses | 2 Anos Não Mobilizável | 500€ | sem máximo | Não mobilizável |

As restantes 17 são escalões do Online e do Novos Recursos entre 1,10% e 1,55%, todas acima do limiar de inclusão.
O Crescente 3 anos, a 2,08%, fica de fora pela regra do prazo único acima dos 24 meses.

A 3,25% a 6 meses, o Novos Clientes entraria em quarto lugar na lista toda, logo a seguir ao Banco Best. Isto não é
um ajuste, é uma ausência visível para quem compara. Confirmar no site do Novo Banco e na FIN, e de caminho corrigir
o URL do catálogo.

## 2. Carregosa, NextGen Welcome Boost a 6 meses: diferença com explicação provável

- Nós temos: NextGen Welcome Boost 3 meses 3,00% e 6 meses 2,80%.
- O Excel tem: NextGen Welcome Boost 3 meses 3,00% e **6 meses 3,00%**, mínimo de 1.000€, máximo de 100.000€.
- Nos dois lados, o Depósito Bem-Vindo é 3 meses 3,00% e 6 meses 2,80%, com mínimo de 5.000€.

Os dois produtos são gémeos e diferem no canal e no mínimo. Tudo indica que copiámos o 2,80% do Bem-Vindo para a linha
do NextGen, que afinal paga 3,00% aos 6 meses. Se o Excel estiver certo, são 0,20 pontos a menos numa das entradas
mais visíveis da lista.

A página do Carregosa não abriu hoje, por isso isto fica por confirmar. É o item que mais vale um clique.

## 3. Atlântico Europa: uma taxa a menos e três produtos a faltar

- **DP Global Living, 6 meses:** Excel 2,75%, nós 2,50%. Mínimo de 2.500€ e máximo de 100.000€, novos clientes e
  novos capitais. A nossa entrada é a única que temos deste banco.
- **DP Atlântico**, que não temos: 3 meses 1,75%, 6 meses 1,85%, 12 meses 2,00%, mínimo de 500€ e máximo de 500.000€,
  sem restrição de novos clientes. Três prazos da grelha, todos acima do limiar.
- **Juro Semestral, 24 meses 2,25%**, mínimo de 20.000€, não mobilizável. Também não temos.

## 4. Bankinter: temos um produto, o Excel tem quatro famílias

O nosso ficheiro tem só o Depósito Net Boas Vindas, 6 meses a 3,00%. O Excel tem 31 linhas, das quais estas na grelha:

- Depósito TOP: 3 meses 2,50%, 6 meses 3,00%, 12 meses 2,40%, 24 meses 2,00%, mínimo de 5.000€.
- Depósito Digital: 3 meses 2,75%, mínimo de 5.000€.
- Depósito TOP Premier: 3 e 6 meses 2,50%, 12 meses 2,30%, 24 meses 2,40%, mínimo de 250.000€.
- Depósito Net: escada por montante, de 1,60% a 2,30%, de 500€ a 100.000€.

O TOP a 3,00% aos 6 meses iguala o nosso Net Boas Vindas e tem mínimo mais baixo. Vale a pena decidir quantos destes
entram, porque o Bankinter está claramente sub-representado na lista. A página do Bankinter não abriu hoje.

## 5. ActivoBank, Depósito Especial Flexível: família inteira em falta

Seis linhas na grelha que não temos, todas por escalão de montante: 12 meses 2,50% (mínimo de 250.000€),
12 meses 2,25% (50.000€), 6 meses 2,25% (250.000€), 6 meses 2,15% (50.000€), 12 meses 2,00% (500€),
6 meses 1,80% (500€). O escalão de 500€ é subscritível por qualquer particular e passa o limiar.

O nome já tinha aparecido na secção 2b do relatório de 1 de novembro, na lista de candidatos do catálogo do
ActivoBank, e ficou por seguir. A página do ActivoBank não abriu hoje.

## 6. Banco Best, Depósito Novos Clientes: o prazo não bate

Três fontes, três respostas:

- O nosso JSON: 6 meses, 3,30%.
- O Excel: **3 meses**, 3,30%, mínimo de 500€ e máximo de 250.000€.
- A página do Best, lida hoje: "Depósito Novos Clientes Aniversário", **180 dias**, 3,30%, mínimo de 500€ e máximo de
  250.000€. Mas essa leitura veio truncada e a tabela caiu fora da parte lida em texto verdadeiro.

Os mínimos e máximos batem certo nos três, logo é o mesmo produto. Só o prazo é que diverge, e a taxa está em
quarto lugar da lista, por isso o prazo decide onde o cartão aparece no seletor. Resolver na FIN.

O Excel tem ainda, do Best: Novos Recursos 3 meses 2,85% (mínimo de 500€) e Conta Poupança Crescente 24 meses 1,59%,
nenhum dos dois com correspondência no nosso ficheiro nesses prazos.

## 7. Outras pistas mais pequenas

- **Crédito Agrícola**, do qual temos uma entrada: Depósito Net 6 meses 1,50% e 12 meses 1,55%, Super Crescente
  24 meses 1,57% (mínimo de 500€). Nenhum está na lista.
- **Millennium BCP, Let's Go**, 6 meses 2,00%, mínimo de 25€. Não temos. Confirmar que não exige domiciliação, porque
  quase tudo o resto do BCP no Excel exige e foi excluído.
- **Santander Jovem**, 6 meses 1,60%, mínimo de 50€. Temos 1,30% no Depósito Poupança Plus. Pela regra, um depósito
  com limite de idade entra com a etiqueta `idade_max` e não fica de fora.
- **Banco CTT, DP XL**: Excel 6 meses 1,70%, 12 meses 1,85%, 24 meses 1,90%. O nosso Super DP tem 1,60%, 1,75% e
  1,80%. São produtos diferentes e provavelmente falta-nos o DP XL.
- **Banco Invest, Depósitos a Prazo**: Excel 3 meses 2,00%, 6 meses 2,20%, 12 e 24 meses 2,35%. Nós temos 1,90%,
  2,10% e 2,25%. Cada prazo 0,10 pontos acima do nosso, de forma consistente, o que sugere uma atualização que não
  apanhámos. A página do Banco Invest estava quebrada hoje, com os marcadores do template à vista.
- **CGD**: Caixa Especial 12 Meses, Excel 1,90% contra os nossos 1,65%, e DP 150 Anos 6 meses, Excel 1,85% contra os
  nossos 1,60%. Os dois 0,25 pontos acima. A página da CGD que temos devolve "ESTA PÁGINA NÃO EXISTE".
- **Banco BiG, Depósito a Prazo 12 meses**: Excel 2,25%, nós 2,00%. Mas a página do BiG, que foi lida hoje sem
  problemas, dá 1 ano a 2,00% no Depósito a Prazo e 12 meses a 2,25% no Dep. a Prazo TOP, que tem mínimo de 50.000€.
  O Excel parece ter juntado os dois. **O nosso valor está certo e o do Excel é que confunde produtos.**
- **ABANCA, Depósito 6M** 1,75% (mínimo de 500€) e **Depósito 12M** 1,75%. Não temos.

## 8. Onde o Excel confirma o que já tínhamos

Vale a pena registar, porque é a maior parte do ficheiro:

- **Haitong**: as oito taxas do HB Sem Mobilização e HB Com Mobilização batem ao centésimo com o nosso ficheiro e com
  o que foi lido hoje no site do banco. Três fontes de acordo.
- **Banco BiG, Super Depósito**: 3 meses 4,00% com mínimo de 5.000€ e 6 meses 3,50% com mínimo de 10.000€, máximo
  de 50.000€. Igual nos três sítios.
- **Carregosa Natal e NextGen Christmas Greetings**: 3 meses 2,50%, 6 meses 2,75%, 12 meses 3,00%. Igual.
- **BNI Europa e Finantia**: as grelhas inteiras batem certo com o que foi lido hoje nos sites dos dois bancos. As
  diferenças aparentes são só de nomenclatura, porque o Excel tem uma linha por variante e nós temos um produto com
  um mapa de prazos.

## 9. Nada parece ter desaparecido

Não há nenhum sinal forte de produto nosso que tenha saído do mercado. As entradas que existem só do nosso lado são
ou bancos estrangeiros que o Excel não cobre (Klarna, bunq) ou bancos que o Excel cobre mal (do BPI tem uma única
linha, e nós temos três produtos). A única a olhar é o Openbank DP Novos Clientes Tri a 3 meses 2,30%, que o Excel
não tem em nenhum prazo de 3 meses.

## 10. Da tabela do JRJordao: bancos estrangeiros que não temos

A imagem da tabela do fórum, que o Franklin também enviou, cobre bancos estrangeiros que o Excel não tem. Quatro
nomes que não estão na nossa lista:

- **Easisave, Fixed term deposit**: 12, 24 e 36 meses a 3,30%, 6 e 9 meses a 3,00%, mínimo de 1.000€, juros
  trimestrais, anuais ou na maturidade. A 3,30% nos 12 e nos 24 meses entraria no top cinco da lista inteira. É a
  pista mais valiosa desta secção.
- **MeDirect, Fixed term deposit**: 36 meses a 3,00%, mínimo de 5.000€. Prazo único acima de 24 meses nesta linha,
  por isso só entra se tiver prazos da grelha. Já temos o MeDirect no comparador de poupanças, com 3 meses 1,00%,
  6 meses 1,90%, 12 meses 2,35% e 24 meses 2,40%.
- **BIL, Term deposit**: 12 meses a 3,00%, mínimo de 10.000€.
- **BluOr Bank, Deposit account**: 3,00%, mínimo de 1.000€, com a nota "subscrever depósito sem abrir conta (tem
  custos)". Os 3,00% são o prazo de 60 meses, que fica fora da grelha. Serve de confirmação cruzada à subida do BluOr
  que foi confirmada hoje no site do banco para o comparador de poupanças.

A tabela do fórum tem notas de bonificação Proteste no BAI Europa e no Haitong. Foram ignoradas, como manda a regra.

## Próximo passo

Por ordem de valor, e tudo a precisar de fonte primária antes de entrar:

1. Novo Banco, o banco inteiro, a começar pelos 3,25% a 6 meses. Corrigir também o URL do catálogo.
2. Carregosa NextGen Welcome Boost a 6 meses, 2,80% contra 3,00%.
3. Easisave, que a 3,30% entraria no topo.
4. Atlântico Europa, uma taxa a corrigir e quatro produtos a acrescentar.
5. Prazo do Depósito Novos Clientes do Banco Best, 3 ou 6 meses.
6. Bankinter e ActivoBank Especial Flexível, que são decisões de âmbito e não correções.
7. Banco Invest, CGD e Banco CTT, diferenças pequenas e consistentes que sugerem atualização não apanhada.

Seis destes sete dependem de páginas que não abriram hoje nesta sessão. São exatamente as que o
`verificar_precarios.py` costuma resolver pelo PDF do preçário, e que não correram porque o Action não correu.
