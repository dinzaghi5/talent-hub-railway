from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class ListCreatorHeader(Base):
    __tablename__ = "tb_r_list_creator_header"

    id = Column(Integer, primary_key=True, index=True)
    name_list = Column(String(255), nullable=False)
    total_creator = Column(Integer, server_default="0", default=0)
    
    created_dt = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(50), nullable=True)
    changed_dt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    changed_by = Column(String(50), nullable=True)

    details = relationship("ListCreatorDetail", back_populates="header", cascade="all, delete-orphan")
