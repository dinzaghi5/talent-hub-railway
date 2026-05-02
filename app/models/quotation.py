from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric
from sqlalchemy.sql import func
from app.db.base_class import Base

class QuotationHeader(Base):
    __tablename__ = "tb_r_quotation_header"

    id = Column(Integer, primary_key=True, index=True)
    quotation_code = Column(String(100), unique=True, index=True, nullable=False)
    invoice_code = Column(String(100), nullable=True)
    brand_name = Column(String(255), nullable=False)
    status_quotation = Column(Integer, nullable=False)
    project = Column(String(255), nullable=True)
    quotation_date = Column(Date, nullable=True)
    subtotal = Column(Numeric(18, 2), nullable=True)
    dpp = Column(Numeric(18, 2), nullable=True)
    ppn = Column(Numeric(18, 2), nullable=True)
    grand_total = Column(Numeric(18, 2), nullable=True)

    created_dt = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(50), nullable=True)
    changed_dt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    changed_by = Column(String(50), nullable=True)
