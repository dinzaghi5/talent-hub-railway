from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.schemas.social_media import SocialMediaCreate, SocialMediaResponse, SocialMediaUpdate
from app.services.social_media_service import social_media_service

router = APIRouter()
#DIAS
@router.post("/", response_model=SocialMediaResponse, status_code=status.HTTP_201_CREATED)
async def create_social_media(
    social_media_in: SocialMediaCreate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Create new social media.
    """
    return await social_media_service.create(db, obj_in=social_media_in)

@router.get("/", response_model=List[SocialMediaResponse])
async def read_social_medias(
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Retrieve social medias.
    """
    social_medias = await social_media_service.get_multi(db)
    return social_medias

@router.get("/{social_media_id}", response_model=SocialMediaResponse)
async def read_social_media(
    social_media_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get social media by ID.
    """
    social_media = await social_media_service.get(db, social_media_id=social_media_id)
    if not social_media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Social media not found",
        )
    return social_media

@router.put("/{social_media_id}", response_model=SocialMediaResponse)
async def update_social_media(
    social_media_id: int,
    social_media_in: SocialMediaUpdate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Update a social media.
    """
    social_media = await social_media_service.get(db, social_media_id=social_media_id)
    if not social_media:   
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Social media not found",
        )
    social_media = await social_media_service.update(db, db_obj=social_media, obj_in=social_media_in)
    return social_media

@router.delete("/{social_media_id}", response_model=SocialMediaResponse)
async def delete_social_media(
    social_media_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Delete a social media.
    """
    social_media = await social_media_service.get(db, social_media_id=social_media_id)
    if not social_media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Social media not found",
        )
    await social_media_service.delete(db, social_media_id=social_media_id)
    return social_media
