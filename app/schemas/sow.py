from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class SowBase(BaseModel):
    sow_nm: Optional[str] = None

class SowCreate(SowBase):
    sow_nm: str

class SowUpdate(SowBase):
    pass

class SowResponse(SowBase):
    sow_id: int
    created_dt: Optional[datetime] = None
    changed_dt: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
