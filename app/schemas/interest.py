from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class InterestBase(BaseModel):
    interest_nm: Optional[str] = None

class InterestCreate(InterestBase):
    interest_nm: str

class InterestUpdate(InterestBase):
    pass

class InterestResponse(InterestBase):
    interest_id: int
    created_dt: Optional[datetime] = None
    changed_dt: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
