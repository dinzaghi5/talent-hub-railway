from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class BrandBase(BaseModel):
    brand_nm: Optional[str] = None
    brand_address: Optional[str] = None
    brand_company_name: Optional[str] = None
    brand_email: Optional[str] = None
    brand_pic_1: Optional[str] = None
    brand_pic_2: Optional[str] = None
    brand_pic_3: Optional[str] = None

class BrandCreate(BrandBase):
    brand_nm: str

class BrandUpdate(BrandBase):
    pass

class BrandResponse(BrandBase):
    brand_id: int
    created_dt: Optional[datetime] = None
    changed_dt: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
