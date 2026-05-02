from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.schemas.invoice_header import InvoiceHeaderCreate, InvoiceHeaderResponse, InvoiceHeaderUpdate
from app.services.invoice_header_service import invoice_header_service

router = APIRouter()

@router.post("/", response_model=InvoiceHeaderResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice_header(
    invoice_in: InvoiceHeaderCreate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Create a new invoice header.
    """
    return await invoice_header_service.create(db, obj_in=invoice_in)

@router.get("/", response_model=List[InvoiceHeaderResponse])
async def read_invoice_headers(
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Retrieve invoice headers.
    """
    return await invoice_header_service.get_multi(db)

@router.get("/{invoice_code}", response_model=InvoiceHeaderResponse)
async def read_invoice_header(
    invoice_code: str,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get invoice header by invoice_code.
    """
    invoice = await invoice_header_service.get(db, invoice_code=invoice_code)
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice header not found",
        )
    return invoice

@router.put("/{invoice_code}", response_model=InvoiceHeaderResponse)
async def update_invoice_header(
    invoice_code: str,
    invoice_in: InvoiceHeaderUpdate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Update an invoice header.
    """
    invoice = await invoice_header_service.get(db, invoice_code=invoice_code)
    if not invoice:   
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice header not found",
        )
    return await invoice_header_service.update(db, db_obj=invoice, obj_in=invoice_in)

@router.delete("/{invoice_code}", response_model=InvoiceHeaderResponse)
async def delete_invoice_header(
    invoice_code: str,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Delete an invoice header.
    """
    invoice = await invoice_header_service.get(db, invoice_code=invoice_code)
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice header not found",
        )
    await invoice_header_service.delete(db, invoice_code=invoice_code)
    return invoice
