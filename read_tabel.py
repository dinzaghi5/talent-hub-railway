import fitz
doc = fitz.open('d:/PROJECT/CODE/TALEND_HUB/BE/tabel.pdf')
page = doc[0]
with open('d:/PROJECT/CODE/TALEND_HUB/BE/tabel_content.txt', 'w', encoding='utf-8') as f:
    f.write(page.get_text())
print("Extracted text from tabel.pdf")
