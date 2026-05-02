from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base_class import Base

class SocialMedia(Base):
    __tablename__ = "tb_m_social_media"

    social_media_id = Column(Integer, primary_key=True, index=True)
    social_media_nm = Column(String, nullable=False)
    base_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    created_dt = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=True)
    changed_dt = Column(DateTime(timezone=True), onupdate=func.now())
    changed_by = Column(String, nullable=True)
