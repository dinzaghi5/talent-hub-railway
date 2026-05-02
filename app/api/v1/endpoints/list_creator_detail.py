from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union

from app.api import deps
from app.schemas.list_creator_detail import ListCreatorDetailCreate, ListCreatorDetailResponse, ListCreatorDetailUpdate
from app.services.list_creator_detail_service import list_creator_detail_service

router = APIRouter()

@router.post("/", response_model=List[ListCreatorDetailResponse], status_code=status.HTTP_201_CREATED)
async def create_list_creator_detail(
    obj_in: List[ListCreatorDetailCreate],
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Create new List Creator Detail(s).
    """
    return await list_creator_detail_service.create_multi(db, objs_in=obj_in)

@router.get("/", response_model=List[ListCreatorDetailResponse])
async def read_list_creator_details(
    header_id: int = None,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Retrieve List Creator Details. Optionally filter by header_id.
    """
    if header_id:
        return await list_creator_detail_service.get_by_header(db, header_id=header_id)
    return await list_creator_detail_service.get_multi(db)

@router.get("/{id}", response_model=ListCreatorDetailResponse)
async def read_list_creator_detail(
    id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get List Creator Detail by ID.
    """
    obj = await list_creator_detail_service.get(db, id=id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List Creator Detail not found",
        )
    return obj

@router.put("/{id}", response_model=ListCreatorDetailResponse)
async def update_list_creator_detail(
    id: int,
    obj_in: ListCreatorDetailUpdate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Update a List Creator Detail.
    """
    obj = await list_creator_detail_service.get(db, id=id)
    if not obj:   
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List Creator Detail not found",
        )
    obj = await list_creator_detail_service.update(db, db_obj=obj, obj_in=obj_in)
    return obj

@router.delete("/{id}", response_model=ListCreatorDetailResponse)
async def delete_list_creator_detail(
    id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Delete a List Creator Detail.
    """
    obj = await list_creator_detail_service.get(db, id=id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List Creator Detail not found",
        )
    await list_creator_detail_service.delete(db, id=id)
    return obj
