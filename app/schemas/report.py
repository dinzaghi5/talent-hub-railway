from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ReportBase(BaseModel):
    name: Optional[str] = None
    link: Optional[str] = None
    followers: Optional[int] = None
    er: Optional[Decimal] = None
    avg_view_all_content: Optional[Decimal] = None
    avg_view_branded_content: Optional[Decimal] = None
    rate_reels: Optional[Decimal] = None
    rate: Optional[Decimal] = None
    creator_username: Optional[str] = None
    quotation_id: Optional[int] = None
    quotation_code: Optional[str] = None

class ReportCreate(ReportBase):
    name: str

class ReportUpdate(ReportBase):
    pass

class ReportResponse(ReportBase):
    id: int
    created_dt: Optional[datetime] = None
    created_by: Optional[str] = None
    changed_dt: Optional[datetime] = None
    changed_by: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
