import fitz

doc = fitz.open(r'C:\Users\ferre\OneDrive\Documentos\PROJETOS PROGRAMAÇÃO\PFP\input_pfp produção\PP0250326.pdf')
text = ''
for page in doc:
    text += page.get_text()
print(text)
