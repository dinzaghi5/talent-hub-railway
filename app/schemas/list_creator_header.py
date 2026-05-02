from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ListCreatorHeaderBase(BaseModel):
    name_list: Optional[str] = None
    total_creator: Optional[int] = 0

class ListCreatorHeaderCreate(ListCreatorHeaderBase):
    name_list: str

class ListCreatorHeaderUpdate(ListCreatorHeaderBase):
    pass

class ListCreatorHeaderResponse(ListCreatorHeaderBase):
    id: int
    created_dt: Optional[datetime] = None
    created_by: Optional[str] = None
    changed_dt: Optional[datetime] = None
    changed_by: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
