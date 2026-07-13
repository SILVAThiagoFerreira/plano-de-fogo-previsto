# DATA_SCHEMA

## Entrada CSV
Campos mínimos:
- `Number`
- `X`
- `Y`
- `Z`
- `Z_Toe`
- `Length`
- `Azimuth`
- `Angle`
- `DesignCharge`
- `Stemming`
- `Subdrilling`
- `DetonatingTime`

Regras adicionais:
- `Number` deve ser um inteiro positivo.

## Saída Excel
Ordem fixa:
1. `Plano`
2. `Tipo`
3. `id`
4. `y`
5. `x`
6. `z (crest)`
7. `z (toe)`
8. `profundidade prevista`
9. `azimute`
10. `inclinacao`
11. `cargas previstas`
12. `tampao previsto`
13. `subperfuracao`
14. `diametro`
15. `DetonatingTime`

## Regras de formato
- Texto do ID preservado como string.
- Campos numéricos com 1 casa decimal, exceto `x` e `y` com 4 casas decimais.
- Uma única aba: `DADOS_FUROS`.
