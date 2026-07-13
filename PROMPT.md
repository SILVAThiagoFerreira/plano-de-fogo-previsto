# PROMPT

Use este projeto como um pipeline de dados com contrato fixo.

## Interpretação obrigatória
- Não assumir nome de arquivo fora do config.
- Não assumir estrutura de CSV sem validar o schema.
- Não misturar leitura com processamento.
- Não alterar a ordem do output sem atualizar a documentação e os testes.

## Como trabalhar
1. Ler `SPEC.md` e `DATA_SCHEMA.md`.
2. Verificar `config.json`.
3. Localizar ponto de entrada em `main.py`.
4. Alterar módulos específicos apenas quando necessário.
5. Atualizar documentação sempre que a regra de negócio mudar.
