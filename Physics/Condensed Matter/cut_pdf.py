from PyPDF2 import PdfReader, PdfWriter

# Caminho do arquivo original (será substituído pelo PDF que o usuário enviar)
input_path = "Solid State Physics Ashcroft - OCR.pdf"
output_path = "Solid State Physics Ashcroft - OCR First pages.pdf"

# Abrir o PDF original
reader = PdfReader(input_path)
writer = PdfWriter()

# Adicionar as primeiras 10 páginas
for i in range(min(20, len(reader.pages))):
    writer.add_page(reader.pages[i])

# Salvar o novo PDF
with open(output_path, "wb") as f_out:
    writer.write(f_out)

