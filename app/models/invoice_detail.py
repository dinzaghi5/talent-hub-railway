from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.sql import func
from app.db.base_class import Base

class InvoiceDetail(Base):
    __tablename__ = "tb_r_invoice_detail"

    # assumed an 'id' column as primary key for SQLAlchemy ORM support
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    invoice_code = Column(String(100), nullable=True)
    quotation_code = Column(String(100), nullable=True)
    client_name = Column(String(255), nullable=True)
    Description = Column("description", String(255), nullable=True)
    sow = Column(String(100), nullable=True)
    Platform = Column("platform", String(100), nullable=True)
    cost = Column(Numeric(18,2), server_default="0")
    bank = Column(String(100), nullable=True)
    account_no = Column(String(100), nullable=True)
    account_name = Column(String(100), nullable=True)
    subtotal = Column(Numeric(18,2), server_default="0")
    dpp = Column(Numeric(18,2), server_default="0")
    ppn = Column(Numeric(18,2), server_default="0")
    grand_total = Column(Numeric(18,2), server_default="0")

    created_dt = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(50), nullable=True)
    changed_dt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    changed_by = Column(String(50), nullable=True)
