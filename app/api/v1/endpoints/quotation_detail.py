from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.schemas.quotation_detail import QuotationDetailCreate, QuotationDetailResponse, QuotationDetailUpdate
from app.services.quotation_detail_service import quotation_detail_service

router = APIRouter()

@router.post("/", response_model=List[QuotationDetailResponse], status_code=status.HTTP_201_CREATED)
async def create_quotation_details(
    details_in: List[QuotationDetailCreate],
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Create new quotation details (bulk).
    """
    return await quotation_detail_service.create_multi(db, objs_in=details_in)

@router.get("/", response_model=List[QuotationDetailResponse])
async def read_quotation_details(
    db: AsyncSession = Depends(deps.get_db),
    header_id: int | None = None
):
    """
    Retrieve quotation details. Pass header_id to filter by header.
    """
    if header_id is not None:
        return await quotation_detail_service.get_by_header(db, header_id=header_id)
    return await quotation_detail_service.get_multi(db)

@router.get("/{detail_id}", response_model=QuotationDetailResponse)
async def read_quotation_detail(
    detail_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get quotation detail by ID.
    """
    detail = await quotation_detail_service.get(db, detail_id=detail_id)
    if not detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation detail not found",
        )
    return detail

@router.put("/{detail_id}", response_model=QuotationDetailResponse)
async def update_quotation_detail(
    detail_id: int,
    detail_in: QuotationDetailUpdate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Update a quotation detail.
    """
    detail = await quotation_detail_service.get(db, detail_id=detail_id)
    if not detail:   
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation detail not found",
        )
    detail = await quotation_detail_service.update(db, db_obj=detail, obj_in=detail_in)
    return detail

@router.delete("/{detail_id}", response_model=QuotationDetailResponse)
async def delete_quotation_detail(
    detail_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Delete a quotation detail.
    """
    detail = await quotation_detail_service.get(db, detail_id=detail_id)
    if not detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation detail not found",
        )
    await quotation_detail_service.delete(db, detail_id=detail_id)
    return detail
