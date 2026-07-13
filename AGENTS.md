# AGENTS.md

## O que este repo faz
Converte CSV de perfuração em Excel padronizado para PFP. Trate como pipeline de dados, não como script solto.

## Fonte de verdade
- `main.py` é o entrypoint; ele chama `src.pipeline.run`.
- `config.json` concentra caminhos, nomes de aba, padrões de ID e colunas.
- `SPEC.md` e `DATA_SCHEMA.md` definem ordem e formato da saída.

## Estrutura útil
- Código ativo fica em `src/` (`reader.py`, `validator.py`, `processor.py`, `writer.py`, `pipeline.py`, `config_loader.py`).
- `generate_corrected_aba2_final.py` e `old/` são legado; não use como base para mudanças novas.

## Regras do pipeline
- Aceite apenas um CSV por execução, em `input/`.
- O CSV real de `input/opit.csv` inclui `DetonatingTime`; use o arquivo real ao validar schema de entrada.
- ID do plano pode vir de PDF, depois XLSX, depois nome do arquivo, depois entrada interativa.
- A saída deve ter uma única aba `DADOS_FUROS`.
- Preserve o ID como texto.
- `x` e `y` usam 4 casas decimais; os demais numéricos usam 1.
- Não altere a ordem das colunas sem atualizar `SPEC.md`, `DATA_SCHEMA.md` e testes.

## Como rodar
- App: `python main.py --config config.json`
- Testes: `python -m unittest discover -s tests`
- Teste focalizado: `python -m unittest tests.test_smoke.SmokeTest.test_output_schema`

## Mudanças
- Validação deve ser explícita; ambiguidades e falhas de schema devem interromper a execução.
- Se mudar schema, formato, regra de ID ou nome de arquivo, atualize `config.json` e a documentação correspondente.
