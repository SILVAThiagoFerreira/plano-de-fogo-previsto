#!/usr/bin/env python3
"""
Script para limpar a pasta input - versão AUTOMÁTICA
Remove todos os arquivos EXCETO os arquivos originais
"""

from pathlib import Path
import os

input_dir = Path(r"C:\Users\ferre\OneDrive\Documentos\PROJETOS PROGRAMAÇÃO\PFP\input_pfp produção")

# Arquivos que devem ser mantidos
arquivos_originais = {"holes.csv", "PP0250326.pdf", "PP0250326.xlsx"}

print("="*70)
print("LIMPANDO PASTA INPUT - MODO AUTOMÁTICO")
print("="*70)
print(f"Pasta: {input_dir}\n")

# Listar todos os arquivos
arquivos_encontrados = list(input_dir.glob("*"))

print("Arquivos encontrados na pasta:")
for arquivo in arquivos_encontrados:
    print(f"  - {arquivo.name}")

# Identificar arquivos a remover
arquivos_a_remover = [f for f in arquivos_encontrados if f.name not in arquivos_originais]

print(f"\n{'='*70}")
print(f"Arquivos que SERÃO REMOVIDOS: {len(arquivos_a_remover)}")
print(f"{'='*70}")

if arquivos_a_remover:
    for arquivo in arquivos_a_remover:
        print(f"  - {arquivo.name}")
    
    print(f"\n{'='*70}")
    print("** EXECUTANDO REMOÇÃO AUTOMÁTICA **")
    print(f"{'='*70}")
    
    for arquivo in arquivos_a_remover:
        try:
            if arquivo.is_file():
                arquivo.unlink()
                print(f"  ✓ Removido: {arquivo.name}")
            elif arquivo.is_dir():
                # Se for pasta, remover recursivamente
                import shutil
                shutil.rmtree(arquivo)
                print(f"  ✓ Pasta removida: {arquivo.name}/")
        except Exception as e:
            print(f"  ✗ Erro ao remover {arquivo.name}: {e}")
    
    print(f"\n{'='*70}")
    print("✓ LIMPEZA CONCLUÍDA!")
    print(f"{'='*70}")
else:
    print("✓ Nenhum arquivo a remover. Pasta já está limpa!")

print(f"\nArquivos remanescentes na pasta input:")
arquivos_finais = list(input_dir.glob("*"))
for arquivo in arquivos_finais:
    print(f"  - {arquivo.name}")