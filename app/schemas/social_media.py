from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class SocialMediaBase(BaseModel):
    social_media_nm: Optional[str] = None
    base_url: Optional[str] = None

class SocialMediaCreate(SocialMediaBase):
    social_media_nm: str

class SocialMediaUpdate(SocialMediaBase):
    is_active: Optional[bool] = None

class SocialMediaResponse(SocialMediaBase):
    social_media_id: int
    is_active: bool
    created_dt: Optional[datetime] = None
    changed_dt: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
