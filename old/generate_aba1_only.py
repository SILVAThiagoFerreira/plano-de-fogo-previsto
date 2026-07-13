import pandas as pd
import numpy as np
from pathlib import Path

# Caminhos dos arquivos
csv_file = Path(r"C:\Users\ferre\OneDrive\Documentos\PROJETOS PROGRAMAÇÃO\PFP\input_pfp produção\holes.csv")
output_dir = Path(r"C:\Users\ferre\OneDrive\Documentos\PROJETOS PROGRAMAÇÃO\PFP\output\PP0250326")

# Ler CSV
df = pd.read_csv(csv_file, skipinitialspace=True)

print("="*70)
print("GERANDO EXCEL COM APENAS ABA 1 - DADOS_FUROS")
print("="*70)

# ABA 1 - DADOS_FUROS
dados_furos = pd.DataFrame({
    "id": df['Number'].astype(str),
    "y": df['Y'],
    "x": df['X'],
    "z": df['Z'],
    "profundidade prevista": df['Length'].round(1),
    "azimute": df['Azimuth'].round(1),
    "inclinação": df['Angle'].round(1),
    "cargas previstas": df['DesignCharge'].round(1),
    "tampão previsto": df['Stemming'].round(1),
    "subperfuração": df['Subdrilling'].round(1)
})

print(f"Total de furos: {len(dados_furos)}")
print("\nPrimeiras 3 linhas:")
print(dados_furos.head(3).to_string(index=False))

# Salvar Excel com APENAS ABA 1
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "DADOS_FUROS_PP0250326.xlsx"

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    dados_furos.to_excel(writer, sheet_name='DADOS_FUROS', index=False)
    
    # Ajustar largura das colunas
    worksheet = writer.sheets['DADOS_FUROS']
    for i, col in enumerate(dados_furos.columns):
        col_letter = chr(65 + i)
        worksheet.column_dimensions[col_letter].width = 15

print("\n" + "="*70)
print(f"ARQUIVO GERADO: {output_file.name}")
print(f"Local: {output_file}")
print(f"Conteúdo: APENAS ABA 1 - DADOS_FUROS")
print(f"Total de furos: {len(dados_furos)}")
print("="*70)