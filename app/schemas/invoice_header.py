from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class InvoiceHeaderBase(BaseModel):
    quotation_code: Optional[str] = None
    client_name: Optional[str] = None

class InvoiceHeaderCreate(InvoiceHeaderBase):
    pass

class InvoiceHeaderUpdate(InvoiceHeaderBase):
    pass

class InvoiceHeaderResponse(InvoiceHeaderBase):
    invoice_code: Optional[str] = None
    created_dt: Optional[datetime] = None
    created_by: Optional[str] = None
    changed_dt: Optional[datetime] = None
    changed_by: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
