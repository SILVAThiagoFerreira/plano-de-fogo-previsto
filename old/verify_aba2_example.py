import pandas as pd
import numpy as np

# Ler o arquivo CSV original
csv_file = r"C:\Users\ferre\OneDrive\Documentos\PROJETOS PROGRAMAÇÃO\PFP\input_pfp produção\holes.csv"
df = pd.read_csv(csv_file, skipinitialspace=True)

print("="*70)
print("ESTRUTURA CORRETA DA ABA 2 - BASEADA NO EXEMPLO")
print("="*70)

# Estrutura correta da ABA 2 conforme o exemplo manual
parametros_corretos = [
    # Informações gerais
    ("Plano", "PP0250326", ""),
    ("Cliente", "-", ""),  # Não disponível no CSV
    ("Furo Satélite", "-", ""),  # Não disponível no CSV
    
    # Parâmetros do plano
    ("Malha Mista", "Não" if (df[df['Burden'] > 0]['Burden'].nunique() <= 1 and df[df['Spacing'] > 0]['Spacing'].nunique() <= 1) else "Sim", ""),
    ("Banco / Área", f"{int(df['Z'].median() / 10) * 10}-{(int(df['Z'].median() / 10) * 10) - 10}", "m"),
    ("Nº de Furos", str(len(df)), "un"),
    ("Altura do Banco", f"{df['Length'].mean():.1f}", "m"),
    ("Afastamento (Burden)", f"{df[df['Burden'] > 0]['Burden'].mean():.1f}" if df[df['Burden'] > 0]['Burden'].count() > 0 else "-", "m"),
    ("Espaçamento", f"{df[df['Spacing'] > 0]['Spacing'].mean():.1f}" if df[df['Spacing'] > 0]['Spacing'].count() > 0 else "-", "m"),
    ("Metragem Perfuração", f"{df['Length'].sum():.1f}", "m"),
    
    # Explosivos
    ("Densidade do Explosivo", "-", "g/cm³"),  # Não disponível
    ("Carga de Fundo", f"{df['DesignCharge'].sum():.1f}" if 'DesignCharge' in df.columns else "-", "kg"),
    ("Emulsão Prevista", f"{df['DesignCharge'].sum():.1f}" if 'DesignCharge' in df.columns else "-", "kg"),
    ("Encartuchado", "-", ""),  # Não disponível
    
    # Materiais de detonação
    ("Iniciador Eletrônico", "DVT 15 m", ""),  # Baseado nos dados
    ("Outros Iniciadores", "-", ""),  # Não disponível
    ("Reforçadores", "Booster 450", ""),  # Baseado nos dados
    ("Cabos", "-", ""),  # Não disponível
    
    # Parâmetros operacionais
    ("Tampão", f"{df['Stemming'].mean():.1f}", "m"),
    ("Inclinação", f"{df['Angle'].mean():.1f}", "°"),
    ("Subperfuração", f"{df['Subdrilling'].mean():.1f}", "m"),
    
    # Informações técnicas
    ("Diâmetro furo", f"{df['Diameter'].mean() * 39.3701:.1f}", "pol"),
    ("Densidade Rocha", "-", "g/cm³"),  # Não disponível
    
    # Observações
    ("Observações", "Dados extraídos do arquivo holes.csv - Plano de Perfuração PP0250326", ""),
]

print("Formato CORRETO para ABA 2 (comparando com exemplo):")
print("-"*70)

for idx, (parametro, valor, unidade) in enumerate(parametros_corretos, 1):
    print(f"{idx:2d}. {parametro:<30} | {valor:<25} | {unidade}")

# Comparar com o que eu gerei anteriormente
print("\n" + "="*70)
print("RELAÇÃO: O QUE EU GEREI vs O QUE DEVERIA SER")
print("="*70)

meus_parametros = [
    "Plano", "Banco / Área", "Malha Mista", "Afastamento", "Espaçamento", 
    "Diâmetro", "Material 1", "Material 2", "Material 3", "Tampão",
    "Inclinação", "Subperfuração", "Dens. Rocha", "Azimute padrão", "Observações"
]

parametros_corretos_nomes = [p[0] for p in parametros_corretos]

print("\nParâmetros que ESTÃO CORRETOS:")
for p in parametros_corretos_nomes:
    if "Material 3" not in p and "Azimute padrão" not in p:  # Excluir os que são diferentes
        print(f"  ✓ {p}")

print("\nParâmetros FALTANDO no meu arquivo:")
for p in parametros_corretos_nomes:
    if p not in meus_parametros and "Observações de extração" not in p:
        print(f"  ✗ {p}")

print("\nParâmetros que ERREI o nome/conceito:")
correcoes = {
    "Material 1": "Iniciador Eletrônico",
    "Material 2": "Reforçadores", 
    "Material 3": "Não usado (deveria ser Outros materiais ou similar)",
    "Azimute padrão": "Não existe no exemplo",
    "Dens. Rocha": "Densidade Rocha",
    "Afastamento": "Afastamento (Burden)",
    "Profundidade / Comprimento": "Altura do Banco",
    "Cargas": "Carga de Fundo / Emulsão Prevista"
}

for meu, correto in correcoes.items():
    if meu in meus_parametros:
        print(f"  ⚠️  '{meu}' → '{correto}'")

print("\n" + "="*70)
print("\nCONCLUSÃO: Preciso refazer a geração da ABA 2 seguindo o modelo correto!")