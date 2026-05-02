from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    fullname: Optional[str] = None
    phone: Optional[str] = None
    role_id: Optional[int] = None

class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str
    fullname: str
    role_id: int

class UserUpdate(BaseModel):
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    fullname: Optional[str] = None
    phone: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    user_id: int
    role_id: int
    is_active: bool
    created_dt: Optional[datetime] = None
    changed_dt: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
