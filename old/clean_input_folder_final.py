#!/usr/bin/env python3
"""
Script para limpar a pasta input - versão FINAL
Remove todos os arquivos EXCETO os arquivos originais
"""

from pathlib import Path
import shutil

input_dir = Path(r"C:\Users\ferre\OneDrive\Documentos\PROJETOS PROGRAMAÇÃO\PFP\input_pfp produção")

# Arquivos que devem ser mantidos
arquivos_originais = {"holes.csv", "PP0250326.pdf", "PP0250326.xlsx"}

print("="*70)
print("LIMPANDO PASTA INPUT - VERSAO FINAL")
print("="*70)
print(f"Pasta: {input_dir}\n")

# Listar todos os arquivos
arquivos_encontrados = list(input_dir.glob("*"))

print("Arquivos encontrados:")
for arquivo in arquivos_encontrados:
    print(f"  - {arquivo.name}")

# Identificar arquivos a remover
arquivos_a_remover = [f for f in arquivos_encontrados if f.name not in arquivos_originais]

print(f"\n{'='*70}")
print(f"Arquivos a remover: {len(arquivos_a_remover)}")
if arquivos_a_remover:
    for arquivo in arquivos_a_remover:
        print(f"  - {arquivo.name}")

# Executar remoção
print(f"\n{'='*70}")
print("EXECUTANDO REMOCAO")
print(f"{'='*70}")

for arquivo in arquivos_a_remover:
    try:
        if arquivo.is_file():
            arquivo.unlink()
            print(f"  [OK] Removido: {arquivo.name}")
        elif arquivo.is_dir():
            shutil.rmtree(arquivo)
            print(f"  [OK] Pasta removida: {arquivo.name}/")
    except Exception as e:
        print(f"  [ERRO] {arquivo.name}: {e}")

print(f"\n{'='*70}")
print("LIMPEZA CONCLUIDA")
print(f"{'='*70}")

print(f"\nArquivos remanescentes:")
for arquivo in input_dir.glob("*"):
    print(f"  - {arquivo.name}")