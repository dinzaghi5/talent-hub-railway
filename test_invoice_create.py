import asyncio
from app.db.session import AsyncSessionLocal
from app.schemas.invoice_detail import InvoiceDetailCreate
from app.services.invoice_detail_service import create_invoice_detail

async def main():
    async with AsyncSessionLocal() as session:
        data = {
            "invoice_code": "1",
            "quotation_code": "QT20260408001",
            "client_name": 0,
            "Description": "string",
            "sow": "1",
            "Platform": "string",
            "cost": 0,
            "bank": "string",
            "account_no": "string",
            "account_name": "string",
            "subtotal": 0,
            "dpp": 0,
            "ppn": 0,
            "grand_total": 0,
            "created_by": "string",
            "changed_by": "string"
        }
        detail = InvoiceDetailCreate(**data)
        try:
            await create_invoice_detail(session, detail)
            print("Success")
        except Exception as e:
            print(f"Error: {e}")

asyncio.run(main())
