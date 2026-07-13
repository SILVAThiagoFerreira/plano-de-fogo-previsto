# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**PFP Generator** - A Python tool for converting drilling plan CSV data into standardized Excel spreadsheets for "Plano de Fogo Previsto" (PFP) - Portuguese mining/blasting planning system.

**Purpose**: Automate extraction of drilling data from mining plans into structured Excel format for operational use.

## Project Structure

```
PFP/
├── input/                          # Input data folders
│   ├── pp/                         # Production Plans (Planos de Produção)
│   │   ├── pp.csv                  # Drilling hole data
│   │   ├── PP{ID}.pdf             # PDF plan (ID source)
│   │   └── PP{ID}.xlsx            # Excel plan (fallback)
│   └── pc/                         # Presplit Plans (Planos de Pre-corte)
├── output/                         # Generated files
│   └── {TIPO}{ID}/                 # Output folder structure
│       └── {TIPO}{ID}_PREV.xlsx   # Generated Excel file
├── old/                            # Deprecated scripts
├── AGENTS.md                       # Project documentation
└── generate_corrected_aba2_final.py # Main script v1.1
```

## Development Commands

### Running the Main Script
```bash
python generate_corrected_aba2_final.py
```

### Required Dependencies
```bash
pip install pandas openpyxl numpy pdfplumber
```

### Python Version
- **Primary**: Python 3.13.13 (as detected in environment)
- **Compatible**: Python 3.8+ (based on library usage)

## Architecture

### Data Flow
1. **Input**: CSV drilling data + PDF/Excel plans → `input/{pp|pc}/`
2. **Processing**: Script detects plan type automatically, extracts ID from PDF/Excel
3. **Output**: Standardized Excel with specific column structure → `output/{TIPO}{ID}_PREV.xlsx`

### Key Components
- **Type Detection**: Automatically detects PP (Production) vs PC (Presplit) based on folder structure
- **ID Extraction**: Prioritizes PDF → Excel → User input for 6-digit plan ID
- **Validation**: 7 automatic validations ensure output format compliance
- **Column Mapping**: Maps CSV columns to standardized Excel format with specific rules

### File Naming Conventions
| Type | Pattern | Example |
|------|---------|---------|
| Input CSV | `PP*.csv` or `PC*.csv` | `input/PC0250326.csv` |
| PDF Plan | `PP{ID}.pdf` or `PC{ID}.pdf` | `PP0250326.pdf` |
| Output Excel | `{TIPO}{ID}_PREV.xlsx` | `PP0250326_PREV.xlsx` |

## Development Guidelines

### Script Rules
- **Only 1 sheet**: Must contain exactly `DADOS_FUROS` sheet
- **12 columns**: Specific column order and formatting requirements
- **No PROMPT GPT**: This sheet is explicitly forbidden
- **Column width**: All columns must be 15 characters wide
- **Decimal formatting**: 1 decimal place for numeric fields

### Validation Requirements
The script includes 7 automatic validations that must pass:
1. Correct file naming pattern
2. Only `DADOS_FUROS` sheet exists
3. No `PROMPT GPT` sheet
4. All 12 required columns present in correct order
5. Column widths = 15 characters
6. Exactly 1 sheet in file
7. Plan and Type columns correctly populated

### Important Constraints
- **Never modify data values** - only formatting/rounding allowed
- **Never add additional sheets** - violates core requirements
- **Never change column order** - breaks compatibility
- **Never remove validations** - compromises system integrity

## Script Status

### Active Scripts
- `generate_corrected_aba2_final.py` (v1.1) - **Current main script**

### Deprecated Scripts (do not use)
- All scripts in `/old/` directory are obsolete
- Includes `generate_aba1_only.py`, `generate_aba2_correct.py`, etc.

## Project History

### Version 1.1 (Current)
- Automatic PP/PC detection by filename prefix
- PDF ID extraction priority
- Added "Plano" and "Tipo" columns (total 15 columns)
- Flat input/output structure (`input/` and `output/`)

### Version 1.0
- Initial implementation
- Removed "PROMPT GPT" sheet requirement
- Established validation framework

## Common Tasks

### Adding New Data Fields
1. Add column to `DADOS_FUROS` sheet mapping
2. Update validation checks for new column count
3. Ensure proper formatting rules

### Modifying ID Extraction
- Update `extrair_id_do_plano_pdf()` or `extrair_id_do_plano_excel()` functions
- Maintain fallback order: PDF → Excel → User input

### Debugging Validation Failures
- Check specific error message for which validation failed
- Review AGENTS.md Section 10 for validation details
- Ensure input files follow required naming conventions

## Important Notes

- Always consult AGENTS.md before making changes - it contains detailed technical specifications
- The project follows strict Portuguese mining terminology and formatting requirements
- Input data structure is specific to drilling/blasting operations
- Output format is designed for operational use in mining environments