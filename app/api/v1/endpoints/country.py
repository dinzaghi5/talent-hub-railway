from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.schemas.country import CountryCreate, CountryResponse, CountryUpdate
from app.services.country_service import country_service

router = APIRouter()

@router.post("/", response_model=CountryResponse, status_code=status.HTTP_201_CREATED)
async def create_country(
    country_in: CountryCreate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Create new country.
    """
    return await country_service.create(db, obj_in=country_in)

@router.get("/", response_model=List[CountryResponse])
async def read_countries(
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Retrieve countries.
    """
    return await country_service.get_multi(db)

@router.get("/{country_id}", response_model=CountryResponse)
async def read_country(
    country_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get country by ID.
    """
    country = await country_service.get(db, country_id=country_id)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found",
        )
    return country

@router.put("/{country_id}", response_model=CountryResponse)
async def update_country(
    country_id: int,
    country_in: CountryUpdate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Update a country.
    """
    country = await country_service.get(db, country_id=country_id)
    if not country:   
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found",
        )
    country = await country_service.update(db, db_obj=country, obj_in=country_in)
    return country

@router.delete("/{country_id}", response_model=CountryResponse)
async def delete_country(
    country_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Delete a country.
    """
    country = await country_service.get(db, country_id=country_id)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found",
        )
    await country_service.delete(db, country_id=country_id)
    return country
