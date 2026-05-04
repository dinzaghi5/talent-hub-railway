from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class Brand(Base):
    __tablename__ = "tb_m_brand"

    brand_id = Column(Integer, primary_key=True, index=True)
    brand_nm = Column(String, nullable=False)
    brand_address = Column(String, nullable=True)
    brand_company_name = Column(String, nullable=True)
    brand_email = Column(String, nullable=True)
    brand_pic_1 = Column(String, nullable=True)
    brand_pic_2 = Column(String, nullable=True)
    brand_pic_3 = Column(String, nullable=True)
    inisial = Column(String, nullable=True)
    
    created_dt = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=True)
    changed_dt = Column(DateTime(timezone=True), onupdate=func.now())
    changed_by = Column(String, nullable=True)
