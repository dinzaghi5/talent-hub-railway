from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core import security
from app.core.config import settings
from app.schemas.token import Token, Login, TokenWithUser
from app.services.auth_service import auth_service

router = APIRouter()

@router.post("/login", response_model=TokenWithUser)
async def login_access_token(
    login_data: Login,
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    """
    Login with identifier (email, username, or phone) and password.
    """
    user = await auth_service.authenticate(
        db, identifier=login_data.identifier, password=login_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email/username or password"
        )
    elif not user.get('o_is_active'):
        raise HTTPException(status_code=400, detail="Inactive user")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Use user_id as subject
    return {
        "access_token": security.create_access_token(
            user.get('o_user_id'), expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "user": {
            "user_id": user.get('o_user_id'),
            "fullname": user.get('o_fullname'),
            "role": user.get('o_role_nm'),
            "is_active": user.get('o_is_active'),
            "email": user.get('o_email'),
            "phone": user.get('o_phone')
        }
    }
