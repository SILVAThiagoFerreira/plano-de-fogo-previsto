import shutil
from pathlib import Path

# Diretórios
base_dir = Path(r"C:\Users\ferre\OneDrive\Documentos\PROJETOS PROGRAMAÇÃO\PFP")
input_dir = base_dir / "input_pfp produção"
output_dir = base_dir / "output"
plano_nome = "PP0250326"

print("Reorganizando estrutura de pastas...")
print(f"Base: {base_dir}")
print(f"Input: {input_dir}")
print(f"Output: {output_dir}")

# 1. Criar pasta output na raiz
output_dir.mkdir(exist_ok=True)
print(f"✓ Pasta output criada na raiz: {output_dir}")

# 2. Criar pasta PP0250326 dentro de output
plano_output_dir = output_dir / plano_nome
plano_output_dir.mkdir(exist_ok=True)
print(f"✓ Pasta {plano_nome} criada em output: {plano_output_dir}")

# 3. Localizar a pasta PP0250326 atual (dentro de input)
atual_plano_dir = input_dir / plano_nome
if not atual_plano_dir.exists():
    print(f"✗ Pasta {plano_nome} não encontrada em {input_dir}")
    exit(1)

# 4. Mover todo o conteúdo de PP0250326 para output/PP0250326
print(f"\nMovendo arquivos de {atual_plano_dir} para {plano_output_dir}")
for item in atual_plano_dir.glob("*"):
    if item.is_file():
        destino = plano_output_dir / item.name
        shutil.move(str(item), str(destino))
        print(f"  - {item.name}")
    elif item.is_dir():
        # Mover diretório inteiro
        destino = plano_output_dir / item.name
        shutil.move(str(item), str(destino))
        print(f"  - Diretorio {item.name}/")

# 5. Remover a pasta PP0250326 antiga (agora vazia)
if atual_plano_dir.exists() and not list(atual_plano_dir.glob("*")):
    atual_plano_dir.rmdir()
    print(f"✓ Pasta antiga removida: {atual_plano_dir}")

print(f"\n{'='*50}")
print("REORGANIZAÇÃO CONCLUÍDA!")
print(f"{'='*50}")
print(f"\nEstrutura final:")
print(f"  PFP/")
print(f"  ├── input_pfp produção/  (arquivos de entrada)")
print(f"  └── output/")
print(f"      └── PP0250326/")
for f in plano_output_dir.glob("*"):
    if f.is_file():
        print(f"          ├── {f.name}")
    elif f.is_dir():
        print(f"          └── {f.name}/")
        for subf in f.glob("*"):
            print(f"              ├── {subf.name}")
print(f"\nDiretório completo: {plano_output_dir}")