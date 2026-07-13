# SPEC

## Objetivo
Converter planilhas CSV de perfuração em Excel padronizado para uso operacional e rastreável.

## Entradas
- CSV em `input/`.
- PDF e/ou XLSX para extração do ID do plano.
- O CSV real de `input/opit.csv` inclui `DetonatingTime`.

## Decisões de negócio
- `PP` mapeia para `Production`.
- `PC` mapeia para `Presplit`.
- A coluna `Plano` recebe o ID extraído.
- A coluna `Number` deve conter inteiros positivos; `0` e valores não inteiros são inválidos.
- A ordem oficial é: `Plano`, `Tipo`, `id`, `y`, `x`, `z (crest)`, `z (toe)`, `profundidade prevista`, `azimute`, `inclinacao`, `cargas previstas`, `tampao previsto`, `subperfuracao`, `diametro`, `DetonatingTime`.
- O ID é preservado como texto.
- `x` e `y` devem ser exibidos com 4 casas decimais; os demais campos numéricos seguem 1 casa decimal.
- Quando existir mais de uma fonte possível para ID, a prioridade é PDF, depois Excel, depois nome de arquivo, depois entrada interativa.

## Validações
- Deve existir exatamente um CSV por execução.
- O CSV deve conter todas as colunas mínimas exigidas, incluindo `DetonatingTime`.
- O Excel final deve conter uma única aba chamada `DADOS_FUROS`.
- O nome do arquivo final deve seguir `{TIPO}{ID}_PREV.xlsx`.

## Erros
- Qualquer ambiguidade na origem dos dados deve interromper a execução.
- Qualquer falha de schema deve impedir a geração do Excel.
