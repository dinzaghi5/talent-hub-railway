from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CityBase(BaseModel):
    city_nm: Optional[str] = None
    country_id: Optional[int] = None

class CityCreate(CityBase):
    city_nm: str
    country_id: int

class CityUpdate(CityBase):
    pass

class CityResponse(CityBase):
    city_id: int
    created_dt: Optional[datetime] = None
    changed_dt: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
