from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class Interest(Base):
    __tablename__ = "tb_m_interest"

    interest_id = Column(Integer, primary_key=True, index=True)
    interest_nm = Column(String, nullable=False)
    
    created_dt = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=True)
    changed_dt = Column(DateTime(timezone=True), onupdate=func.now())
    changed_by = Column(String, nullable=True)
