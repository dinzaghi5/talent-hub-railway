from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.pdf import InvoiceCreate
from app.services.pdf_service import pdf_service

router = APIRouter()

@router.post("/invoice")
async def generate_invoice_pdf(
    data: InvoiceCreate
):
    """
    Generate Invoice PDF based on input data.
    Format matches the company invoice template.
    """
    pdf_buffer = pdf_service.create_invoice_pdf(data)

    # Filename: INVOICE - invoice_no (or just INVOICE if empty)
    if data.invoice_no:
        filename = f"INVOICE - {data.invoice_no}.pdf"
    else:
        filename = "INVOICE.pdf"

    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers=headers
    )
