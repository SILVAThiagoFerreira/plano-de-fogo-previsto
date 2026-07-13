import pandas as pd
import numpy as np
from pathlib import Path

# Caminhos dos arquivos
data_dir = Path(r"C:\Users\ferre\OneDrive\Documentos\PROJETOS PROGRAMAÇÃO\PFP\input_pfp produção")
base_dir = Path(r"C:\Users\ferre\OneDrive\Documentos\PROJETOS PROGRAMAÇÃO\PFP")
csv_file = data_dir / "holes.csv"

# Ler CSV
df = pd.read_csv(csv_file, skipinitialspace=True)

print("="*70)
print("GERANDO ABA 2 - PROMPT GPT - CORRETAMENTE")
print("="*70)

# Lista CORRETA de parâmetros conforme exemplo manual
# OBS: Valores que não têm no CSV ficam como "-" ou vazio
parametros = []

# ===== INFORMAÇÕES GERAIS =====
parametros.append({"Parâmetro": "CLIENTE", "Valor": "-", "Unidade de medida": ""})  # Não disponível no CSV
parametros.append({"Parâmetro": "FURO SATÉLITE", "Valor": "-", "Unidade de medida": ""})  # Não disponível

# ===== PARÂMETROS DO PLANO =====
# Malha Mista (verificar se há múltiplos valores de Burden/Spacing)
burden_unicos = df[df['Burden'] > 0]['Burden'].nunique()
spacing_unicos = df[df['Spacing'] > 0]['Spacing'].nunique()
malha_mista = "Sim" if burden_unicos > 1 or spacing_unicos > 1 else "Não"
parametros.append({"Parâmetro": "Malha Mista", "Valor": malha_mista, "Unidade de medida": ""})

# Banco / Área (intervalo de cotas)
cota_media = df['Z'].median()
cota_base = (int(cota_media / 10)) * 10
banco_area = f"{cota_base}-{cota_base-10}"
parametros.append({"Parâmetro": "Banco / Área", "Valor": banco_area, "Unidade de medida": "m"})

# Nº de Furos
parametros.append({"Parâmetro": "Nº de Furos", "Valor": str(len(df)), "Unidade de medida": "un"})

# Altura do Banco (profundidade média)
parametros.append({"Parâmetro": "Altura do Banco", "Valor": f"{df['Length'].mean():.1f}", "Unidade de medida": "m"})

# Afastamento (Burden médio)
burden_valores = df[df['Burden'] > 0]['Burden']
if len(burden_valores) > 0:
    parametros.append({"Parâmetro": "Afastamento", "Valor": f"{burden_valores.mean():.1f}", "Unidade de medida": "m"})
else:
    parametros.append({"Parâmetro": "Afastamento", "Valor": "-", "Unidade de medida": "m"})

# Espaçamento
spacing_valores = df[df['Spacing'] > 0]['Spacing']
if len(spacing_valores) > 0:
    parametros.append({"Parâmetro": "Espaçamento", "Valor": f"{spacing_valores.mean():.1f}", "Unidade de medida": "m"})
else:
    parametros.append({"Parâmetro": "Espaçamento", "Valor": "-", "Unidade de medida": "m"})

# Metragem Perfuração (total)
parametros.append({"Parâmetro": "Metragem Perfuração", "Valor": f"{df['Length'].sum():.1f}", "Unidade de medida": "m"})

# Densidade do Explosivo (não disponível no CSV)
parametros.append({"Parâmetro": "Densidade do Explosivo", "Valor": "-", "Unidade de medida": "g/cm³"})

# Carga de Fundo (total de explosivo)
if 'DesignCharge' in df.columns:
    parametros.append({"Parâmetro": "Carga de Fundo", "Valor": f"{df['DesignCharge'].sum():.1f}", "Unidade de medida": "kg"})
else:
    parametros.append({"Parâmetro": "Carga de Fundo", "Valor": "-", "Unidade de medida": "kg"})

# Emulsão Prevista (igual à carga total)
if 'DesignCharge' in df.columns:
    parametros.append({"Parâmetro": "Emulsão Prevista", "Valor": f"{df['DesignCharge'].sum():.1f}", "Unidade de medida": "kg"})
else:
    parametros.append({"Parâmetro": "Emulsão Prevista", "Valor": "-", "Unidade de medida": "kg"})

# Encartuchado (não disponível)
parametros.append({"Parâmetro": "Encartuchado", "Valor": "-", "Unidade de medida": ""})

# ===== MATERIAIS DE DETONAÇÃO =====
# Iniciador Eletrônico - extrair do campo Detonators
detonadores = df['Detonators'].dropna().unique()
detonador_principal = detonadores[0] if len(detonadores) > 0 else "-"
parametros.append({"Parâmetro": "Iniciador Eletrônico", "Valor": str(detonador_principal), "Unidade de medida": ""})

# Outros Iniciadores (não disponível)
parametros.append({"Parâmetro": "Outros Iniciadores", "Valor": "-", "Unidade de medida": ""})

# Reforçadores - extrair do campo Boosters
boosters = df['Boosters'].dropna().unique()
booster_principal = boosters[0] if len(boosters) > 0 else "-"
parametros.append({"Parâmetro": "Reforçadores", "Valor": str(booster_principal), "Unidade de medida": ""})

# Cabos (não disponível)
parametros.append({"Parâmetro": "Cabos", "Valor": "-", "Unidade de medida": ""})

# ===== PARÂMETROS DE PERFURAÇÃO =====
# Tampão
parametros.append({"Parâmetro": "Tampão", "Valor": f"{df['Stemming'].mean():.1f}", "Unidade de medida": "m"})

# Inclinação
parametros.append({"Parâmetro": "Inclinação", "Valor": f"{df['Angle'].mean():.1f}", "Unidade de medida": "°"})

# Subperfuração
parametros.append({"Parâmetro": "Subperfuração", "Valor": f"{df['Subdrilling'].mean():.1f}", "Unidade de medida": "m"})

# Diâmetro furo
parametros.append({"Parâmetro": "Diâmetro furo", "Valor": f"{df['Diameter'].mean() * 39.3701:.1f}", "Unidade de medida": "pol"})

# Densidade Rocha
parametros.append({"Parâmetro": "Densidade Rocha", "Valor": "-", "Unidade de medida": "g/cm³"})

# ===== INFORMAÇÕES FINAIS =====
# Empresa Responsável (não disponível)
parametros.append({"Parâmetro": "EMPRESA RESPONSÁVEL", "Valor": "-", "Unidade de medida": ""})

# Nome (não disponível)
parametros.append({"Parâmetro": "NOME", "Valor": "-", "Unidade de medida": ""})

# Data (não disponível - e NÃO deve ser incluída conforme regras!)
# parametros.append({"Parâmetro": "DATA", "Valor": "-", "Unidade de medida": ""})

# Observações Gerais (texto longo)
observacoes = "Dados extraídos do plano PP0250326. Verificar esquema de amarração. Ponto de isolamento: respeitar área de segurança."
parametros.append({"Parâmetro": "OBSERVAÇÕES", "Valor": observacoes, "Unidade de medida": ""})

# OBS (campo adicional)
parametros.append({"Parâmetro": "OBS", "Valor": "-", "Unidade de medida": ""})

# Criar DataFrame
df_aba2 = pd.DataFrame(parametros)

print(f"\nTotal de parâmetros: {len(parametros)}")
print("\nPreview dos primeiros 10 parâmetros:")
print(df_aba2.head(10).to_string(index=False))

# Verificar se estamos seguindo o modelo
campos_obrigatorios = ["CLIENTE", "FURO SATÉLITE", "Malha Mista", "Banco / Área", "Nº de Furos",
                      "Altura do Banco", "Afastamento", "Espaçamento", "Metragem Perfuração",
                      "Densidade do Explosivo", "Carga de Fundo", "Emulsão Prevista",
                      "Iniciador Eletrônico", "Reforçadores", "Tampão", "Inclinação",
                      "Subperfuração", "OBSERVAÇÕES"]

presentes = [p for p in campos_obrigatorios if p in df_aba2['Parâmetro'].values]
faltando = [p for p in campos_obrigatorios if p not in df_aba2['Parâmetro'].values]

print(f"\n✓ Parâmetros presentes: {len(presentes)}/{len(campos_obrigatorios)}")
print(f"✗ Faltando: {faltando}")

# Salvar arquivo Excel
target_dir = Path(r"C:\Users\ferre\OneDrive\Documentos\PROJETOS PROGRAMAÇÃO\PFP\output\PP0250326")
target_dir.mkdir(parents=True, exist_ok=True)

# Ler o arquivo CSV novamente para criar a ABA 1 também
df_furos = pd.read_csv(csv_file, skipinitialspace=True)

# Criar ABA 1
dados_furos = pd.DataFrame({
    "id": df_furos['Number'].astype(str),
    "y": df_furos['Y'],
    "x": df_furos['X'], 
    "z": df_furos['Z'],
    "profundidade prevista": df_furos['Length'].round(1),
    "azimute": df_furos['Azimuth'].round(1),
    "inclinação": df_furos['Angle'].round(1),
    "cargas previstas": df_furos['DesignCharge'].round(1),
    "tampão previsto": df_furos['Stemming'].round(1),
    "subperfuração": df_furos['Subdrilling'].round(1)
})

# Salvar arquivo Excel
output_file = target_dir / "DADOS_PERFURACAO_CORRETO.xlsx"

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    dados_furos.to_excel(writer, sheet_name='DADOS_FUROS', index=False)
    df_aba2.to_excel(writer, sheet_name='PROMPT GPT', index=False)

print(f"\n" + "="*70)
print(f"✓ ARQUIVO GERADO: {output_file}")
print(f"✓ ABA 1: {len(dados_furos)} furos")
print(f"✓ ABA 2: {len(df_aba2)} parâmetros")
print("="*70)