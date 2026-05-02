from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal

class QuotationDetailBase(BaseModel):
    header_id: Optional[int] = None
    link_foto: Optional[str] = None
    creator_name: Optional[str] = None
    creator_username: Optional[str] = None
    creator_post: Optional[int] = 0
    followers: Optional[int] = 0
    sow_id: Optional[int] = None
    quantity: Optional[int] = 0
    id_medsos: Optional[int] = None
    rate: Optional[Decimal] = 0
    total_cost: Optional[Decimal] = 0
    er: Optional[Decimal] = None
    avg_view: Optional[Decimal] = None
    avg_brand_view: Optional[Decimal] = None

class QuotationDetailCreate(QuotationDetailBase):
    header_id: int
    creator_name: str

class QuotationDetailUpdate(QuotationDetailBase):
    pass

class QuotationDetailResponse(QuotationDetailBase):
    id: int
    header_id: int
    creator_name: str
    created_dt: Optional[datetime] = None
    created_by: Optional[str] = None
    changed_dt: Optional[datetime] = None
    changed_by: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
