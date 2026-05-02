from app.schemas.pdf import InvoiceCreate, InvoiceItem
import datetime, fitz
from app.services.pdf_service import pdf_service

data = InvoiceCreate(
    invoice_no='131/VITALIS/XI/2025', quotation_no='106/VITALIS/IX/2025',
    date=datetime.date(2025, 11, 18),
    client_name='VITALIS', client_company='PT UNZA VITALIS',
    client_email='contact@wipro-unza.co.id',
    client_address='bluegreen Office Tower, Jl. Lkr. Luar Barat No 88 7th Floor,\nRT.6/RW.1, Kembangan Utara, Kec Kembangan  Kota Jakarta Barat',
    items=[InvoiceItem(description='CindyPrisillia', sow='1x IG reels Tag collab', amount=40000000.0)],
    ppn_percentage=12.0, bank_name='Bank Mandiri', account_no='17300-2804-1995',
    city='Jakarta', signatory_name='Donna Bella Apri San', signatory_title='Direktur',
    terms='Please send payment within 30 days of receiving this invoice.\nThere will be a 1.5% interest charge per month on late invoices.'
)
buf = pdf_service.create_invoice_pdf(data)
with open('test_invoice5.pdf', 'wb') as f:
    f.write(buf.read())
pix = fitz.open('test_invoice5.pdf')[0].get_pixmap(dpi=150)
pix.save(r'C:\Users\ASUS\.gemini\antigravity\brain\b96c9650-6b7f-4732-83f2-ee26c41974c4\invoice_v5.png')
print('OK')
