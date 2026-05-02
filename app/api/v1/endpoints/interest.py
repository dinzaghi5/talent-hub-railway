from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.schemas.interest import InterestCreate, InterestResponse, InterestUpdate
from app.services.interest_service import interest_service

router = APIRouter()

@router.post("/", response_model=InterestResponse, status_code=status.HTTP_201_CREATED)
async def create_interest(
    interest_in: InterestCreate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Create new interest.
    """
    return await interest_service.create(db, obj_in=interest_in)

@router.get("/", response_model=List[InterestResponse])
async def read_interests(
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Retrieve interests.
    """
    return await interest_service.get_multi(db)

@router.get("/{interest_id}", response_model=InterestResponse)
async def read_interest(
    interest_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get interest by ID.
    """
    interest = await interest_service.get(db, interest_id=interest_id)
    if not interest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interest not found",
        )
    return interest

@router.put("/{interest_id}", response_model=InterestResponse)
async def update_interest(
    interest_id: int,
    interest_in: InterestUpdate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Update a interest.
    """
    interest = await interest_service.get(db, interest_id=interest_id)
    if not interest:   
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interest not found",
        )
    interest = await interest_service.update(db, db_obj=interest, obj_in=interest_in)
    return interest

@router.delete("/{interest_id}", response_model=InterestResponse)
async def delete_interest(
    interest_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Delete a interest.
    """
    interest = await interest_service.get(db, interest_id=interest_id)
    if not interest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interest not found",
        )
    await interest_service.delete(db, interest_id=interest_id)
    return interest
