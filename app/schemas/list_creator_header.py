from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ListCreatorHeaderBase(BaseModel):
    name_list: Optional[str] = None
    total_creator: Optional[int] = 0

class ListCreatorHeaderCreate(ListCreatorHeaderBase):
    name_list: str

class ListCreatorHeaderUpdate(ListCreatorHeaderBase):
    pass

class ListCreatorDetailBulkCreate(BaseModel):
    link_foto: Optional[str] = None
    creator_name: str
    creator_username: Optional[str] = None
    creator_post: Optional[int] = 0
    followers: Optional[int] = 0
    sow_id: Optional[int] = None
    quantity: Optional[int] = 0
    id_medsos: Optional[int] = None
    rate: Optional[Decimal] = Decimal("0.00")
    er: Optional[Decimal] = None
    avg_view: Optional[Decimal] = None
    avg_brand_view: Optional[Decimal] = None

class ListCreatorWithDetailCreate(ListCreatorHeaderCreate):
    details: list[ListCreatorDetailBulkCreate]

class ListCreatorHeaderResponse(ListCreatorHeaderBase):
    id: int
    created_dt: Optional[datetime] = None
    created_by: Optional[str] = None
    changed_dt: Optional[datetime] = None
    changed_by: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
