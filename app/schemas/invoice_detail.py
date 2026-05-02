from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class InvoiceDetailBase(BaseModel):
    invoice_code: Optional[str] = None
    quotation_code: Optional[str] = None
    client_name: Optional[str] = None
    Description: Optional[str] = None
    sow: Optional[str] = None
    Platform: Optional[str] = None
    cost: Optional[Decimal] = Decimal('0.00')
    bank: Optional[str] = None
    account_no: Optional[str] = None
    account_name: Optional[str] = None
    subtotal: Optional[Decimal] = Decimal('0.00')
    dpp: Optional[Decimal] = Decimal('0.00')
    ppn: Optional[Decimal] = Decimal('0.00')
    grand_total: Optional[Decimal] = Decimal('0.00')
    created_by: Optional[str] = None
    changed_by: Optional[str] = None

class InvoiceDetailCreate(InvoiceDetailBase):
    pass

class InvoiceDetailUpdate(InvoiceDetailBase):
    pass

class InvoiceDetailResponse(InvoiceDetailBase):
    id: int
    created_dt: Optional[datetime] = None
    changed_dt: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class InvoiceDetailBulkCreate(BaseModel):
    details: List[InvoiceDetailCreate]
