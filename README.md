# Comparador de depósitos a prazo: dados e verificação quinzenal

```
data/depositos.json                  fonte de verdade da lista (23 depósitos, 1 set 2026)
scripts/verificar_depositos.py       compara o JSON com o Excel do Economia e Finanças, verifica as páginas de cada depósito e vasculha o catálogo de cada banco à procura de depósitos novos
verificacao/TAREFA.md                passos da tarefa mensal (Claude Code) e regras
verificacao/AAAA-MM/relatorio.md     relatório de cada mês (gerado)
.github/workflows/verificar-depositos.yml   corre o script no dia 1 e abre um issue com o relatório
```

## Fluxo quinzenal (dias 1 e 16)

1. Dias 1 e 16: o workflow corre o script e abre um issue "Depósitos a prazo: verificação AAAA-MM"
   com as diferenças face ao Excel, as percentagens encontradas nos sites e os pendentes.
2. Claude Code (tarefa `verificacao/TAREFA.md`) lê as páginas guardadas e a tabela do
   JRJordao, e escreve o resumo Mudou / Novo / Desapareceu / Não consegui confirmar.
3. Franklin aprova. Só então se edita `data/depositos.json` e a página.

O script nunca escreve em `data/depositos.json`.

## Correr à mão

```
pip install requests openpyxl beautifulsoup4 pypdf
python3 scripts/verificar_depositos.py              # Excel + sites dos bancos
python3 scripts/verificar_depositos.py --sem-bancos # só o Excel
```

## Formato de `data/depositos.json`

Um objeto por depósito. `prazos` tem a TANB por prazo em meses (e mínimo/máximo
quando diferem do geral). `mobilizacao`: `nao` | `total` | `parcial` | `semestre`.
`novos`: `clientes` | `montantes` | null. `url_fin` é o link da Ficha de Informação
Normalizada, que o script também lê quando existe. `a_confirmar: true` mantém o
depósito na lista de pendentes do relatório.

## Limites conhecidos

- O Haitong não publica as taxas na página: só no preçário e na FIN. O script avisa,
  mas a confirmação é manual.
- O Fórum do Investidor bloqueia pedidos automáticos e a tabela do JRJordao é uma
  imagem: fica para a leitura em Claude Code (passo 3 da tarefa).
- Se o Economia e Finanças mudar os cabeçalhos do Excel, o relatório diz "FALHOU" na
  secção 1 e o resto continua a funcionar.
