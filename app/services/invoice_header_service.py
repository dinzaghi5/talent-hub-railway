from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.invoice_header import InvoiceHeader
from app.schemas.invoice_header import InvoiceHeaderCreate, InvoiceHeaderUpdate

class InvoiceHeaderService:
    async def _generate_invoice_code(self, db: AsyncSession) -> str:
        from datetime import date
        from sqlalchemy import func
        today_str = date.today().strftime("%Y%m%d")
        prefix = f"INV{today_str}"

        # Count existing codes with today's prefix
        result = await db.execute(
            select(func.count(InvoiceHeader.invoice_code)).where(
                InvoiceHeader.invoice_code.like(f"{prefix}%")
            )
        )
        count = result.scalar() or 0
        next_number = count + 1
        return f"{prefix}{next_number:03d}"

    async def get(self, db: AsyncSession, invoice_code: str) -> InvoiceHeader | None:
        result = await db.execute(select(InvoiceHeader).filter(InvoiceHeader.invoice_code == invoice_code))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession) -> list[InvoiceHeader]:
        result = await db.execute(select(InvoiceHeader))
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, obj_in: InvoiceHeaderCreate) -> InvoiceHeader:
        invoice_code = await self._generate_invoice_code(db)
        db_obj = InvoiceHeader(
            invoice_code=invoice_code,
            quotation_code=obj_in.quotation_code,
            client_name=obj_in.client_name,
            created_by="SYSTEM"
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: InvoiceHeader, obj_in: InvoiceHeaderUpdate) -> InvoiceHeader:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db_obj.changed_by = "SYSTEM"
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, invoice_code: str) -> InvoiceHeader | None:
        obj = await self.get(db, invoice_code)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

invoice_header_service = InvoiceHeaderService()
