import pandas as pd
import numpy as np

# Caminho do arquivo de exemplo
example_file = r"C:\Users\ferre\OneDrive\Documentos\PROJETOS PROGRAMAÇÃO\PFP\Plano de fogo previsto gerado para exemplo e estudo\Plano de Fogo Previsto - 250426_B.xls"

print("="*70)
print("ANÁLISE COMPLETA DA ABA 2 - EXEMPLO MANUAL")
print("="*70)

# Ler a aba "Capa" (segunda aba)
capa = pd.read_excel(example_file, sheet_name='Capa')

print(f"\nDimensões da planilha: {capa.shape}")
print(f"Colunas: {list(capa.columns)}")

# Descobrir onde estão os parâmetros
print("\n" + "="*70)
print("PROCURANDO PARÂMETROS NA ABA CAPA")
print("="*70)

# Vamos procurar pela lista de parâmetros
parametros_encontrados = []

# Procurar em todas as células por padrões conhecidos
for row_idx in range(capa.shape[0]):
    for col_idx in range(capa.shape[1]):
        valor = str(capa.iloc[row_idx, col_idx])
        if valor != 'nan' and valor.strip():
            # Verificar se é um parâmetro (possui : ou é maiúsculo e curto)
            if ':' in valor or (len(valor.strip()) < 50 and valor.strip().isupper()):
                parametros_encontrados.append({
                    'row': row_idx,
                    'col': col_idx,
                    'valor': valor.strip()
                })

print(f"\nEncontrados {len(parametros_encontrados)} possíveis parâmetros:")
for p in parametros_encontrados[:10]:  # Mostrar os 10 primeiros
    print(f"  Linha {p['row']}, Col {p['col']}: {p['valor']}")

# Ajustar: a segunda aba não é "PROMPT GPT" mas sim "Capa"
# E os parâmetros são estruturados de forma diferente

print("\n" + "="*70)
print("ANÁLISE PRINCIPAL - ESTRUTURA DOS PARÂMETROS")
print("="*70)

# Tentar extrair os parâmetros organizados
# Pelo que vi, parece ter uma estrutura em colunas

# Vamos ver o conteúdo de cada linha interessante
linhas_interessantes = []
for i in range(min(30, capa.shape[0])):
    for j in range(min(10, capa.shape[1])):
        valor = str(capa.iloc[i, j])
        if valor != 'nan' and valor.strip() and ':' not in valor:
            # Limpar e formatar
            valor_limpo = valor.strip()
            if len(valor_limpo) > 3 and not valor_limpo.startswith('Unnamed'):
                linhas_interessantes.append((i, j, valor_limpo))

print("\nConteúdo organizado por linhas:")
for row, col, val in linhas_interessantes:
    print(f"  [{row},{col}] {val}")

# Salvar análise para estudo
with open(r"C:\Users\ferre\OneDrive\Documentos\PROJETOS PROGRAMAÇÃO\PFP\analise_aba2.txt", 'w', encoding='utf-8') as f:
    f.write("ANÁLISE DA ABA CAPA DO ARQUIVO DE EXEMPLO\n")
    f.write("="*70 + "\n\n")
    f.write(f"Arquivo: {example_file}\n")
    f.write(f"Dimensões: {capa.shape}\n")
    f.write(f"Colunas: {list(capa.columns)}\n\n")
    f.write("CONTEÚDO ORGANIZADO:\n")
    f.write("-"*50 + "\n")
    for row, col, val in linhas_interessantes:
        f.write(f"[{row},{col}] {val}\n")

print("\n" + "="*70)
print("Análise salva em: PFP\analise_aba2.txt")
print("="*70)