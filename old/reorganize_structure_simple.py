import shutil
from pathlib import Path

# Diretorios
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
print(f"Pasta output criada na raiz: {output_dir}")

# 2. Criar pasta PP0250326 dentro de output
plano_output_dir = output_dir / plano_nome
plano_output_dir.mkdir(exist_ok=True)
print(f"Pasta {plano_nome} criada em output: {plano_output_dir}")

# 3. Localizar a pasta PP0250326 atual (dentro de input)
atual_plano_dir = input_dir / plano_nome
if not atual_plano_dir.exists():
    print(f"ERRO: Pasta {plano_nome} nao encontrada em {input_dir}")
    exit(1)

print(f"Pasta atual encontrada: {atual_plano_dir}")

# 4. Mover todo o conteudo de PP0250326 para output/PP0250326
print(f"Movendo arquivos de {atual_plano_dir} para {plano_output_dir}")
for item in atual_plano_dir.glob("*"):
    if item.is_file():
        destino = plano_output_dir / item.name
        shutil.move(str(item), str(destino))
        print(f"  ARQUIVO: {item.name}")
    elif item.is_dir():
        destino = plano_output_dir / item.name
        shutil.move(str(item), str(destino))
        print(f"  PASTA: {item.name}/")

# 5. Remover a pasta PP0250326 antiga (agora vazia)
if atual_plano_dir.exists() and not list(atual_plano_dir.glob("*")):
    atual_plano_dir.rmdir()
    print(f"Pasta antiga removida: {atual_plano_dir}")

print("\n=======================================")
print("REORGANIZACAO CONCLUIDA!")
print("=======================================")
print("\nEstrutura final:")
print(f"  PFP/")
print(f"  ├── input_pfp produção/  (arquivos de entrada)")
print(f"  └── output/")
print(f"      └── PP0250326/")

# Verificar e listar conteudo final
if plano_output_dir.exists():
    print(f"\nConteudo em {plano_output_dir}:")
    for item in sorted(plano_output_dir.glob("*")):
        if item.is_file():
            print(f"  - {item.name}")
        elif item.is_dir():
            print(f"  - {item.name}/")
            for subitem in sorted(item.glob("*")):
                print(f"    - {subitem.name}")

print(f"\nDiretorio completo: {plano_output_dir}")