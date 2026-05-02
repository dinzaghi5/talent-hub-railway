from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean
from sqlalchemy.sql import func
from app.db.base_class import Base

class Report(Base):
    __tablename__ = "tb_r_report"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    link = Column(String(500), nullable=True)
    followers = Column(Integer, nullable=True)
    er = Column(Numeric(5, 2), nullable=True)
    avg_view_all_content = Column(Numeric(18, 2), nullable=True)
    avg_view_branded_content = Column(Numeric(18, 2), nullable=True)
    rate_reels = Column(Numeric(18, 2), nullable=True)
    rate = Column(Numeric(18, 2), nullable=True)
    creator_username = Column(String(255), nullable=True)
    quotation_id = Column(Integer, nullable=True)
    quotation_code = Column(String(50), nullable=True)

    created_dt = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(50), nullable=True)
    changed_dt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    changed_by = Column(String(50), nullable=True)
