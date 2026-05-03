from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.api import deps
from app.schemas.quotation import QuotationCreate, QuotationResponse, QuotationUpdate, QuotationStatusUpdate, QuotationWithDetailCreate
from app.services.quotation_service import quotation_service

router = APIRouter()

@router.post("/", response_model=QuotationResponse, status_code=status.HTTP_201_CREATED)
async def create_quotation(
    quotation_in: QuotationCreate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Create a new quotation.
    quotation_code is auto-generated with format: QT{YYYYMMDD}{3-digit-increment}
    e.g. QT20260408001
    """
    return await quotation_service.create(db, obj_in=quotation_in)

@router.post("/with-details", response_model=QuotationResponse, status_code=status.HTTP_201_CREATED)
async def create_quotation_with_details(
    quotation_in: QuotationWithDetailCreate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Create a new quotation with details.
    """
    return await quotation_service.create_with_details(db, obj_in=quotation_in)

@router.get("/", response_model=List[QuotationResponse])
async def read_quotations(
    status_quotation: Optional[int] = None,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Retrieve quotations. Filter by status_quotation if provided.
    """
    return await quotation_service.get_multi(db, status_quotation=status_quotation)

@router.get("/{quotation_id}", response_model=QuotationResponse)
async def read_quotation(
    quotation_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get quotation by ID.
    """
    quotation = await quotation_service.get(db, quotation_id=quotation_id)
    if not quotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation not found",
        )
    return quotation

@router.put("/{quotation_id}", response_model=QuotationResponse)
async def update_quotation(
    quotation_id: int,
    quotation_in: QuotationUpdate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Update a quotation.
    """
    quotation = await quotation_service.get(db, quotation_id=quotation_id)
    if not quotation:   
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation not found",
        )
    quotation = await quotation_service.update(db, db_obj=quotation, obj_in=quotation_in)
    return quotation

@router.patch("/status/{quotation_id}", response_model=QuotationResponse)
async def update_quotation_status(
    quotation_id: int,
    status_in: QuotationStatusUpdate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Update only status_quotation for a quotation.
    """
    quotation = await quotation_service.get(db, quotation_id=quotation_id)
    if not quotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation not found",
        )
    quotation = await quotation_service.update_status(db, db_obj=quotation, status=status_in.status_quotation)
    return quotation

@router.delete("/{quotation_id}", response_model=QuotationResponse)
async def delete_quotation(
    quotation_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Delete a quotation.
    """
    quotation = await quotation_service.get(db, quotation_id=quotation_id)
    if not quotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation not found",
        )
    await quotation_service.delete(db, quotation_id=quotation_id)
    return quotation
