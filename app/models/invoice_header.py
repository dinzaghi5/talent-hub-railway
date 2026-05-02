from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class InvoiceHeader(Base):
    __tablename__ = "tb_r_invoice_header"

    invoice_code = Column(String(100), primary_key=True, index=True)
    quotation_code = Column(String(100), nullable=True)
    client_name = Column(String(255), nullable=True)
    
    created_dt = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(50), nullable=True)
    changed_dt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    changed_by = Column(String(50), nullable=True)
