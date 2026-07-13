import pandas as pd

# Caminho do arquivo de exemplo
example_file = r"C:\Users\ferre\OneDrive\Documentos\PROJETOS PROGRAMAÇÃO\PFP\Plano de fogo previsto gerado para exemplo e estudo\Plano de Fogo Previsto - 250426_B.xls"

print("Analisando arquivo de exemplo...")
print(f"Arquivo: {example_file}")
print()

# Tentar ler o arquivo Excel
xl = pd.ExcelFile(example_file)
print(f"Abas encontradas: {xl.sheet_names}")
print()

# Ler ABA 2 (deve ser a segunda aba ou 'PROMPT GPT')
if 'PROMPT GPT' in xl.sheet_names:
    aba2 = pd.read_excel(example_file, sheet_name='PROMPT GPT')
    print("ABA 2: PROMPT GPT - encontrada!")
elif len(xl.sheet_names) >= 2:
    aba2 = pd.read_excel(example_file, sheet_name=xl.sheet_names[1])
    print(f"ABA 2: {xl.sheet_names[1]} - usando segunda aba")
else:
    print("Erro: Não há segunda aba no arquivo")
    exit(1)

print(f"\nNúmero de linhas: {len(aba2)}")
print(f"Colunas: {list(aba2.columns)}")

print("\n" + "="*60)
print("CONTEÚDO COMPLETO DA ABA 2:")
print("="*60)

for idx, row in aba2.iterrows():
    if 'Parâmetro' in aba2.columns:
        param = str(row['Parâmetro']) if pd.notna(row['Parâmetro']) else ""
        valor = str(row['Valor']) if pd.notna(row['Valor']) else ""
        unidade = str(row['Unidade de medida']) if pd.notna(row['Unidade de medida']) else ""
    else:
        # Se não houver colunas nomeadas, usar índices
        cols = list(row.values)
        param = str(cols[0]) if len(cols) > 0 else ""
        valor = str(cols[1]) if len(cols) > 1 else ""
        unidade = str(cols[2]) if len(cols) > 2 else ""
    
    print(f"{idx+1:2d}. {param:<30} | {valor:<25} | {unidade}")

print("\n" + "="*60)
print("Resumo dos parâmetros encontrados:")
print("="*60)

# Contar por tipo de parâmetro
parametros = []
for idx, row in aba2.iterrows():
    param = str(row.get('Parâmetro', '')) if pd.notna(row.get('Parâmetro', '')) else f"Linha_{idx+1}"
    parametros.append(param)

print(f"Total: {len(parametros)} parâmetros")
for i, p in enumerate(parametros, 1):
    print(f"  {i}. {p}")