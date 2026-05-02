from sqlalchemy import Column, Float, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class MasterSystem(Base):
    __tablename__ = "tb_m_system"

    system_type = Column(String, nullable=False, primary_key=True)
    system_cd = Column(String, nullable=False, primary_key=True)
    system_val = Column(String)

    created_dt = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=True)
    changed_dt = Column(DateTime(timezone=True), onupdate=func.now())
    changed_by = Column(String, nullable=True)