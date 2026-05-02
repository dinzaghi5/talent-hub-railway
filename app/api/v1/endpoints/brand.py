from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.schemas.brand import BrandCreate, BrandResponse, BrandUpdate
from app.services.brand_service import brand_service

router = APIRouter()

@router.post("/", response_model=BrandResponse, status_code=status.HTTP_201_CREATED)
async def create_brand(
    brand_in: BrandCreate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Create new brand.
    """
    return await brand_service.create(db, obj_in=brand_in)

@router.get("/", response_model=List[BrandResponse])
async def read_brands(
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Retrieve brands.
    """
    return await brand_service.get_multi(db)

@router.get("/{brand_id}", response_model=BrandResponse)
async def read_brand(
    brand_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get brand by ID.
    """
    brand = await brand_service.get(db, brand_id=brand_id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found",
        )
    return brand

@router.put("/{brand_id}", response_model=BrandResponse)
async def update_brand(
    brand_id: int,
    brand_in: BrandUpdate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Update a brand.
    """
    brand = await brand_service.get(db, brand_id=brand_id)
    if not brand:   
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found",
        )
    brand = await brand_service.update(db, db_obj=brand, obj_in=brand_in)
    return brand

@router.delete("/{brand_id}", response_model=BrandResponse)
async def delete_brand(
    brand_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Delete a brand.
    """
    brand = await brand_service.get(db, brand_id=brand_id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found",
        )
    await brand_service.delete(db, brand_id=brand_id)
    return brand
