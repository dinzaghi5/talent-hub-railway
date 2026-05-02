from sqlalchemy import Column, Float, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class KOLDetailModel(Base):
    __tablename__ = "tb_m_kol_detail"

    kol_id = Column(Integer, primary_key=True, index=True)
    kol_account = Column(String, nullable=False)
    total_post = Column(Float)
    avg_like = Column(Float)
    avg_comment = Column(Float)
    avg_reach = Column(Float)
    avg_view = Column(Float)
    avg_brand_view = Column(Float)
    er = Column(Float)
    avg_watch_time = Column(Float)
    last_update = Column(DateTime, nullable=False)
    days = Column(String,nullable=False)
    top_hashtags = Column(String,nullable=True)
    top_mentions = Column(String,nullable=True)
    socmed_type = Column(String,nullable=True)

    created_dt = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=True)
    changed_dt = Column(DateTime(timezone=True), onupdate=func.now())
    changed_by = Column(String, nullable=True)

class KOLHeaderModel(Base):
    __tablename__ = "tb_m_kol_header"

    kol_id = Column(Integer, primary_key=True, index=True)
    kol_account = Column(String, nullable=False)
    kol_name = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    bussiness_category = Column(String, nullable=True)
    followers = Column(Integer, nullable=True)
    following = Column(Integer, nullable=True)
    last_update = Column(DateTime, nullable=False)
    last_post = Column(String, nullable=False)
    socmed_type = Column(String,nullable=True)

    created_dt = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=True)
    changed_dt = Column(DateTime(timezone=True), onupdate=func.now())
    changed_by = Column(String, nullable=True)
