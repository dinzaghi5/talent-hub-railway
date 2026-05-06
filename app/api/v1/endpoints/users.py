from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import user_service

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Create new user.
    """
    # Check if email already exists
    user_email = await user_service.get_by_email(db, email=user_in.email)
    if user_email:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    # Check if username already exists
    user_username = await user_service.get_by_username(db, username=user_in.username)
    if user_username:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    
    # Check if role_id exists
    role_exists = await user_service.check_role_exists(db, role_id=user_in.role_id)
    if not role_exists:
        raise HTTPException(
            status_code=400,
            detail=f"Role ID {user_in.role_id} not found in Master Role database.",
        )

    new_user = await user_service.create(db, user_in=user_in)
    return new_user

@router.get("/", response_model=List[UserResponse])
async def read_users(
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Retrieve users.
    """
    users = await user_service.get_multi(db)
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get user by ID.
    """
    user = await user_service.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Update a user.
    """
    user = await user_service.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Check email uniqueness if changed
    if user_in.email and user_in.email != user.email:
        user_email = await user_service.get_by_email(db, email=user_in.email)
        if user_email:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )

    # Check username uniqueness if changed
    if user_in.username and user_in.username != user.username:
        user_username = await user_service.get_by_username(db, username=user_in.username)
        if user_username:
            raise HTTPException(
                status_code=400,
                detail="The user with this username already exists in the system.",
            )

    # Check role_id validity if changed
    if user_in.role_id is not None and user_in.role_id != user.role_id:
        role_exists = await user_service.check_role_exists(db, role_id=user_in.role_id)
        if not role_exists:
            raise HTTPException(
                status_code=400,
                detail=f"Role ID {user_in.role_id} not found in Master Role database.",
            )

    user = await user_service.update(db, db_obj=user, obj_in=user_in)
    return user

@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Delete a user.
    """
    user = await user_service.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ErrorMessage : User not found",
        )
    await user_service.delete(db, user_id=user_id)
    return user
