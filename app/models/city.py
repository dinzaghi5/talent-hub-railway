from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base_class import Base

class City(Base):
    __tablename__ = "tb_m_city"

    city_id = Column(Integer, primary_key=True, index=True)
    city_nm = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey("tb_m_country.country_id"), nullable=False)
    
    created_dt = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=True)
    changed_dt = Column(DateTime(timezone=True), onupdate=func.now())
    changed_by = Column(String, nullable=True)
