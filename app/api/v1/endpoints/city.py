from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.schemas.city import CityCreate, CityResponse, CityUpdate
from app.services.city_service import city_service

router = APIRouter()

@router.post("/", response_model=CityResponse, status_code=status.HTTP_201_CREATED)
async def create_city(
    city_in: CityCreate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Create new city.
    """
    return await city_service.create(db, obj_in=city_in)

@router.get("/", response_model=List[CityResponse])
async def read_cities(
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Retrieve cities.
    """
    return await city_service.get_multi(db)

@router.get("/{city_id}", response_model=CityResponse)
async def read_city(
    city_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get city by ID.
    """
    city = await city_service.get(db, city_id=city_id)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    return city

@router.put("/{city_id}", response_model=CityResponse)
async def update_city(
    city_id: int,
    city_in: CityUpdate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Update a city.
    """
    city = await city_service.get(db, city_id=city_id)
    if not city:   
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    city = await city_service.update(db, db_obj=city, obj_in=city_in)
    return city

@router.delete("/{city_id}", response_model=CityResponse)
async def delete_city(
    city_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Delete a city.
    """
    city = await city_service.get(db, city_id=city_id)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    await city_service.delete(db, city_id=city_id)
    return city
