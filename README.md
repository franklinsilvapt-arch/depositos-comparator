# Comparador de depósitos a prazo (LiteraciaFinanceira.pt)

Serve o CSS e o JS do comparador via GitHub Pages e guarda a verificação quinzenal dos dados.

```
comparador-depositos.css             estilos do comparador (carregado pela página Webflow)
comparador-depositos.js              gerado a partir de data/depositos.json por scripts/gerar_js.py (não editar à mão)
data/depositos.json                  fonte de verdade da lista e catálogos dos bancos
logos/                               logótipos dos bancos servidos pelo GitHub Pages
scripts/verificar_depositos.py       compara o JSON com o Excel do Economia e Finanças, verifica as páginas de cada depósito e vasculha o catálogo de cada banco
scripts/gerar_js.py                  gera o JS a partir do JSON e do template
scripts/comparador-template.js       lógica do comparador (o bloco de dados é injetado pelo gerador)
verificacao/TAREFA.md                passos da tarefa quinzenal e regras
verificacao/candidatos-AAAA-MM.md    candidatos a incluir, a confirmar nos bancos
.github/workflows/verificar-depositos.yml   corre o script nos dias 1 e 16 e abre um issue com o relatório
.github/workflows/gerar-js.yml       regenera o JS sempre que o JSON ou o template mudam
```

## Fluxo quinzenal (dias 1 e 16)

1. O workflow corre o script e abre um issue "Depósitos a prazo: verificação AAAA-MM-DD".
2. Leitura humana (Claude + Franklin): diferenças, candidatos, FIN, tabela do JRJordao.
3. Franklin aprova. Edita-se só `data/depositos.json`; o JS regenera-se e a página atualiza.

Regra de inclusão: TANB >= 1,00%, depósitos a prazo em euros para particulares, sem restrição de idade nem de domiciliação de ordenado, confirmados no site ou na FIN do banco. Estrangeiros: só a Klarna.
