from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.schemas.invoice_detail import InvoiceDetailCreate, InvoiceDetailUpdate, InvoiceDetailResponse, InvoiceDetailBulkCreate
from app.services import invoice_detail_service

router = APIRouter()

@router.post("/", response_model=InvoiceDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice_detail(
    detail_in: InvoiceDetailCreate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Create a new invoice detail.
    """
    return await invoice_detail_service.create_invoice_detail(db=db, detail=detail_in)

@router.post("/bulk", response_model=List[InvoiceDetailResponse], status_code=status.HTTP_201_CREATED)
async def create_invoice_details_bulk(
    bulk_in: InvoiceDetailBulkCreate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Create multiple invoice details.
    """
    return await invoice_detail_service.create_invoice_details_bulk(db=db, details=bulk_in.details)

@router.get("/", response_model=List[InvoiceDetailResponse])
async def read_invoice_details(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_db),
    invoice_code: str = None
):
    """
    Retrieve invoice details.
    """
    if invoice_code:
        details = await invoice_detail_service.get_invoice_details_by_header(db, invoice_code=invoice_code)
    else:
        details = await invoice_detail_service.get_invoice_details(db, skip=skip, limit=limit)
    return details

@router.get("/{detail_id}", response_model=InvoiceDetailResponse)
async def read_invoice_detail(
    detail_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get invoice detail by ID.
    """
    detail = await invoice_detail_service.get_invoice_detail(db, detail_id=detail_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Invoice detail not found")
    return detail

@router.put("/{detail_id}", response_model=InvoiceDetailResponse)
async def update_invoice_detail(
    detail_id: int,
    detail_in: InvoiceDetailUpdate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Update an invoice detail.
    """
    detail = await invoice_detail_service.get_invoice_detail(db, detail_id=detail_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Invoice detail not found")
        
    updated_detail = await invoice_detail_service.update_invoice_detail(db=db, detail_id=detail_id, detail_update=detail_in)
    return updated_detail

@router.delete("/{detail_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice_detail(
    detail_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Delete an invoice detail.
    """
    detail = await invoice_detail_service.get_invoice_detail(db, detail_id=detail_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Invoice detail not found")
    await invoice_detail_service.delete_invoice_detail(db=db, detail_id=detail_id)
    return None
