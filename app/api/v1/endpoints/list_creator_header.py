from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union

from app.api import deps
from app.schemas.list_creator_header import ListCreatorHeaderCreate, ListCreatorHeaderResponse, ListCreatorHeaderUpdate
from app.services.list_creator_header_service import list_creator_header_service

router = APIRouter()

@router.post("/", response_model=List[ListCreatorHeaderResponse], status_code=status.HTTP_201_CREATED)
async def create_list_creator_header(
    obj_in: List[ListCreatorHeaderCreate],
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Create new List Creator Header(s).
    """
    return await list_creator_header_service.create_multi(db, objs_in=obj_in)

@router.get("/", response_model=List[ListCreatorHeaderResponse])
async def read_list_creator_headers(
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Retrieve List Creator Headers.
    """
    return await list_creator_header_service.get_multi(db)

@router.get("/{id}", response_model=ListCreatorHeaderResponse)
async def read_list_creator_header(
    id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get List Creator Header by ID.
    """
    obj = await list_creator_header_service.get(db, id=id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List Creator Header not found",
        )
    return obj

@router.put("/{id}", response_model=ListCreatorHeaderResponse)
async def update_list_creator_header(
    id: int,
    obj_in: ListCreatorHeaderUpdate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Update a List Creator Header.
    """
    obj = await list_creator_header_service.get(db, id=id)
    if not obj:   
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List Creator Header not found",
        )
    obj = await list_creator_header_service.update(db, db_obj=obj, obj_in=obj_in)
    return obj

@router.delete("/{id}", response_model=ListCreatorHeaderResponse)
async def delete_list_creator_header(
    id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Delete a List Creator Header.
    """
    obj = await list_creator_header_service.get(db, id=id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List Creator Header not found",
        )
    await list_creator_header_service.delete(db, id=id)
    return obj
