from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.invoice_header import InvoiceHeader
from app.models.brand import Brand
from app.schemas.invoice_header import InvoiceHeaderCreate, InvoiceHeaderUpdate

class InvoiceHeaderService:
    def _get_roman_month(self, month: int) -> str:
        roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
        return roman[month - 1]

    async def _generate_invoice_code(self, db: AsyncSession, brand_inisial: str = "DGM") -> str:
        from datetime import date
        from sqlalchemy import func
        today = date.today()
        year = today.year
        month_roman = self._get_roman_month(today.month)
        
        # Clean brand_inisial and use default if empty
        brand = (brand_inisial or "DGM").upper()
        
        prefix = f"INV/{brand}/{year}/{month_roman}/"

        # Count existing codes with this prefix to get the next sequence
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
        # Get brand initial from database
        brand_inisial = "DGM"
        if obj_in.client_name:
            brand_result = await db.execute(select(Brand).filter(Brand.brand_nm == obj_in.client_name))
            brand_obj = brand_result.scalars().first()
            if brand_obj and brand_obj.inisial:
                brand_inisial = brand_obj.inisial

        invoice_code = await self._generate_invoice_code(db, brand_inisial=brand_inisial)
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
