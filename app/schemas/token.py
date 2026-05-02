from typing import Optional
from pydantic import BaseModel

class Login(BaseModel):
    identifier: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenUser(BaseModel):
    user_id: int
    fullname: Optional[str] = None
    role: Optional[str] = None
    is_active: bool
    email: Optional[str] = None
    phone: Optional[str] = None

class TokenWithUser(Token):
    user: TokenUser

class TokenPayload(BaseModel):
    sub: Optional[str] = None
