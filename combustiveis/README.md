# Combustíveis: blocos extra (literaciafinanceira.pt/precos-combustiveis)

Dois blocos novos para a página de combustíveis, carregados por `combustiveis-extra.js` a partir de `extra.json`:

1. **Preço eficiente**: o preço de referência que a ERSE calcula todas as semanas para a gasolina 95 simples e o gasóleo simples (relatório semanal de supervisão dos preços de combustíveis).
2. **Preço médio por marca**: média simples dos preços afixados por posto no portal da DGEG, para marcas com 20 ou mais postos.

`atualizar_extra.py` atualiza as marcas todos os dias pela API da DGEG e tenta ler o PDF da ERSE. As comparações da ERSE com os preços anunciados e com descontos (`eficiente.anterior`) são preenchidas à mão a partir do relatório.

`workflow-combustiveis-extra.yml` só fica ativo depois de copiado para `.github/workflows/`.

Enquanto estiver em teste, a página só carrega `combustiveis-extra.js` no domínio de staging (webflow.io).
