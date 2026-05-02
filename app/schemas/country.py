from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CountryBase(BaseModel):
    country_nm: Optional[str] = None

class CountryCreate(CountryBase):
    country_nm: str

class CountryUpdate(CountryBase):
    pass

class CountryResponse(CountryBase):
    country_id: int
    created_dt: Optional[datetime] = None
    changed_dt: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
