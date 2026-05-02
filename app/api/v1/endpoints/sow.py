from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.schemas.sow import SowCreate, SowResponse, SowUpdate
from app.services.sow_service import sow_service

router = APIRouter()

@router.post("/", response_model=SowResponse, status_code=status.HTTP_201_CREATED)
async def create_sow(
    sow_in: SowCreate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Create new sow.
    """
    return await sow_service.create(db, obj_in=sow_in)

@router.get("/", response_model=List[SowResponse])
async def read_sows(
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Retrieve sows.
    """
    return await sow_service.get_multi(db)

@router.get("/{sow_id}", response_model=SowResponse)
async def read_sow(
    sow_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get sow by ID.
    """
    sow = await sow_service.get(db, sow_id=sow_id)
    if not sow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sow not found",
        )
    return sow

@router.put("/{sow_id}", response_model=SowResponse)
async def update_sow(
    sow_id: int,
    sow_in: SowUpdate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Update a sow.
    """
    sow = await sow_service.get(db, sow_id=sow_id)
    if not sow:   
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sow not found",
        )
    sow = await sow_service.update(db, db_obj=sow, obj_in=sow_in)
    return sow

@router.delete("/{sow_id}", response_model=SowResponse)
async def delete_sow(
    sow_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Delete a sow.
    """
    sow = await sow_service.get(db, sow_id=sow_id)
    if not sow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sow not found",
        )
    await sow_service.delete(db, sow_id=sow_id)
    return sow
