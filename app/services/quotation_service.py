from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, func
from typing import Optional, List
from datetime import date
from app.models.report import Report
from app.models.quotation import QuotationHeader
from app.schemas.quotation import QuotationCreate, QuotationUpdate


class QuotationService:

    async def _generate_quotation_code(self, db: AsyncSession) -> str:
        """
        Generate quotation_code with format: QT{YYYYMMDD}{3-digit-increment}
        e.g. QT20260408001, QT20260408002, ...
        Increment resets every day.
        """
        today_str = date.today().strftime("%Y%m%d")
        prefix = f"QT{today_str}"

        # Count existing codes with today's prefix
        result = await db.execute(
            select(func.count(QuotationHeader.id)).where(
                QuotationHeader.quotation_code.like(f"{prefix}%")
            )
        )
        count = result.scalar() or 0
        next_number = count + 1
        return f"{prefix}{next_number:03d}"

    async def get(self, db: AsyncSession, quotation_id: int) -> QuotationHeader | None:
        result = await db.execute(select(QuotationHeader).filter(QuotationHeader.id == quotation_id))
        return result.scalars().first()

    async def get_by_code(self, db: AsyncSession, quotation_code: str) -> QuotationHeader | None:
        result = await db.execute(select(QuotationHeader).filter(QuotationHeader.quotation_code == quotation_code))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession, *, status_quotation: Optional[int] = None) -> list[QuotationHeader]:
        query = select(QuotationHeader)
        if status_quotation is not None:
            query = query.filter(QuotationHeader.status_quotation == status_quotation)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, obj_in: QuotationCreate) -> QuotationHeader:
        # Auto-generate quotation_code
        quotation_code = await self._generate_quotation_code(db)

        db_obj = QuotationHeader(
            quotation_code=quotation_code,
            invoice_code=obj_in.invoice_code,
            brand_name=obj_in.brand_name,
            status_quotation=obj_in.status_quotation,
            project=obj_in.project,
            quotation_date=obj_in.quotation_date,
            subtotal=obj_in.subtotal,
            dpp=obj_in.dpp,
            ppn=obj_in.ppn,
            grand_total=obj_in.grand_total,
            created_by="SYSTEM"
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: QuotationHeader, obj_in: QuotationUpdate) -> QuotationHeader:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_status(self, db: AsyncSession, *, db_obj: QuotationHeader, status: int) -> QuotationHeader:
        db_obj.status_quotation = status
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, quotation_id: int) -> QuotationHeader | None:
        obj = await self.get(db, quotation_id)
        if obj:
            # Delete related reports
            await db.execute(delete(Report).where(Report.quotation_id == quotation_id))

            await db.delete(obj)
            await db.commit()
        return obj


quotation_service = QuotationService()
