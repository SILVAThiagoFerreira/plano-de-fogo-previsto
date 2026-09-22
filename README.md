# PLANO DE FOGO PREVISTO

Gerador online do PFP para GitHub Pages. A aplicação reproduz o contrato do pipeline local: recebe um CSV de perfuração, um XLSX auxiliar com `ID` e `Diameter` e, opcionalmente, PDF/TXT para identificação do plano. O resultado é baixado como `PP{ID}_PREV.xlsx` ou `PC{ID}_PREV.xlsx`, com a aba `DADOS_FUROS`.

## Uso local

Abra `index.html` em um servidor estático, por exemplo `python -m http.server 8080`, e acesse `http://localhost:8080`.

## Privacidade e compatibilidade

O processamento é feito no navegador. Os arquivos nunca são enviados para um backend. A versão Python original (`main.py` e `src/`) permanece no repositório para execução local e referência das regras de dados.

## Publicação

O conteúdo da raiz é compatível com GitHub Pages e não exige build. Dependências de leitura CSV, XLSX e PDF são carregadas de CDNs públicas com versões fixadas.

## Planilhas modelo

A página disponibiliza dois arquivos para download direto em `assets/modelos/`, preservando os nomes originais fornecidos:

- `Modelo - BLOCOS - SEM FUROS` → `Plano de Fogo - Secundários - .xlsx`
- `Plano Previsto - Produção` → `Plano de Fogo Previsto - .xlsx`

Os arquivos são cópias dos modelos fornecidos para este projeto e não são alterados pelo processamento no navegador.
