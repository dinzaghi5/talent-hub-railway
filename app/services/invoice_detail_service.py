from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.invoice_detail import InvoiceDetail
from app.schemas.invoice_detail import InvoiceDetailCreate, InvoiceDetailUpdate
from typing import List, Optional

async def get_invoice_details(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[InvoiceDetail]:
    result = await db.execute(select(InvoiceDetail).offset(skip).limit(limit))
    return result.scalars().all()

async def get_invoice_detail(db: AsyncSession, detail_id: int) -> Optional[InvoiceDetail]:
    result = await db.execute(select(InvoiceDetail).filter(InvoiceDetail.id == detail_id))
    return result.scalars().first()

async def get_invoice_details_by_header(db: AsyncSession, invoice_code: str) -> List[InvoiceDetail]:
    result = await db.execute(select(InvoiceDetail).filter(InvoiceDetail.invoice_code == invoice_code))
    return result.scalars().all()

async def create_invoice_detail(db: AsyncSession, detail: InvoiceDetailCreate) -> InvoiceDetail:
    db_detail = InvoiceDetail(**detail.model_dump())
    db.add(db_detail)
    await db.commit()
    await db.refresh(db_detail)
    return db_detail

async def create_invoice_details_bulk(db: AsyncSession, details: List[InvoiceDetailCreate]) -> List[InvoiceDetail]:
    db_details = [InvoiceDetail(**detail.model_dump()) for detail in details]
    db.add_all(db_details)
    await db.commit()
    for db_detail in db_details:
        await db.refresh(db_detail)
    return db_details

async def update_invoice_detail(db: AsyncSession, detail_id: int, detail_update: InvoiceDetailUpdate) -> Optional[InvoiceDetail]:
    db_detail = await get_invoice_detail(db, detail_id)
    if db_detail:
        update_data = detail_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_detail, key, value)
        await db.commit()
        await db.refresh(db_detail)
    return db_detail

async def delete_invoice_detail(db: AsyncSession, detail_id: int) -> bool:
    db_detail = await get_invoice_detail(db, detail_id)
    if db_detail:
        await db.delete(db_detail)
        await db.commit()
        return True
    return False

async def delete_invoice_details_by_header(db: AsyncSession, invoice_code: str) -> bool:
    details = await get_invoice_details_by_header(db, invoice_code)
    for detail in details:
        await db.delete(detail)
    await db.commit()
    return True
