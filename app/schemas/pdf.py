from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class QuotationItem(BaseModel):
    description: str
    sow: str
    platform: str
    quantity: int = 1
    cost: float

class QuotationCreate(BaseModel):
    quotation_no: str
    date: date
    brand_name: str
    project_name: str
    kol_name: str
    
    items: List[QuotationItem]
    
    ppn_percentage: float = 11.0
    pic_count: int = 1
    
    # PIC Names
    pic_name_1: Optional[str] = "Donna Bella Hirajati"
    pic_name_2: Optional[str] = "Natawiria"
    pic_name_3: Optional[str] = "Lilik Sujieanto<br/>Director"
    
    # Terms (optional, with defaults if not provided)
    payment_terms: str = "1. The Payment Will be after campaign finish\n2. Due Date 14 Days After Invoice is received"
    revision_terms: str = "1. maximum revisions is 2x (two times). additional revision will be charged propotionally"
    cancellation_terms: str = "1. Cancellation fee after approval quotation by sign or email is 50% from total project amount."

class QuotationCreateNoPic(BaseModel):
    """Schema untuk endpoint /pic1, /pic2, /pic3 — pic_count ditentukan otomatis oleh route."""
    quotation_no: str
    date: date
    brand_name: str
    project_name: str
    kol_name: str
    
    items: List[QuotationItem]
    
    ppn_percentage: float = 11.0
    
    # PIC Names
    pic_name_1: Optional[str] = "Donna Bella Hirajati"
    pic_name_2: Optional[str] = "Natawiria"
    pic_name_3: Optional[str] = "Lilik Sujieanto<br/>Director"
    
    # Terms (optional, with defaults if not provided)
    payment_terms: str = "1. The Payment Will be after campaign finish\n2. Due Date 14 Days After Invoice is received"
    revision_terms: str = "1. maximum revisions is 2x (two times). additional revision will be charged propotionally"
    cancellation_terms: str = "1. Cancellation fee after approval quotation by sign or email is 50% from total project amount."

    def to_quotation_create(self, pic_count: int) -> QuotationCreate:
        return QuotationCreate(
            quotation_no=self.quotation_no,
            date=self.date,
            brand_name=self.brand_name,
            project_name=self.project_name,
            kol_name=self.kol_name,
            items=self.items,
            ppn_percentage=self.ppn_percentage,
            pic_count=pic_count,
            pic_name_1=self.pic_name_1,
            pic_name_2=self.pic_name_2,
            pic_name_3=self.pic_name_3,
            payment_terms=self.payment_terms,
            revision_terms=self.revision_terms,
            cancellation_terms=self.cancellation_terms,
        )

class InvoiceItem(BaseModel):
    description: str          # KOL name / description
    sow: str                  # Statement Of Work
    amount: float

class InvoiceCreate(BaseModel):
    invoice_no: str
    quotation_no: str
    date: date

    # Invoice To (client)
    client_name: str
    client_company: str
    client_email: str
    client_address: str

    # Items
    items: List[InvoiceItem]

    ppn_percentage: float = 12.0

    # Payment method
    bank_name: str = "Bank Mandiri"
    account_no: str = "17300-2804-1995"

    # Signatory
    city: str = "Jakarta"
    signatory_name: str = "Donna Bella Apri San"
    signatory_title: str = "Direktur"

    # Terms
    terms: str = "Please send payment within 30 days of receiving this invoice.\nThere will be a 1.5% interest charge per month on late invoices."
