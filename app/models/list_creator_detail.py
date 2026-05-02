from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class ListCreatorDetail(Base):
    __tablename__ = "tb_r_list_creator_detail"

    id = Column(Integer, primary_key=True, index=True)
    header_id = Column(Integer, ForeignKey("tb_r_list_creator_header.id", ondelete="CASCADE"), nullable=False)
    link_foto = Column(String(500), nullable=True)
    creator_name = Column(String(255), nullable=False)
    creator_username = Column(String(255), nullable=True)
    creator_post = Column(Integer, server_default="0", default=0)
    followers = Column(Integer, server_default="0", default=0)
    sow_id = Column(Integer, ForeignKey("tb_m_sow.sow_id"), nullable=True)
    quantity = Column(Integer, server_default="0", default=0)
    id_medsos = Column(Integer, ForeignKey("tb_m_social_media.social_media_id"), nullable=True)
    rate = Column(Numeric(18, 2), server_default="0.00", default=0.00)
    er = Column(Numeric(5, 2), nullable=True)
    avg_view = Column(Numeric(18, 2), nullable=True)
    avg_brand_view = Column(Numeric(18, 2), nullable=True)

    created_dt = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(50), nullable=True)
    changed_dt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    changed_by = Column(String(50), nullable=True)

    header = relationship("ListCreatorHeader", back_populates="details")
    sow = relationship("Sow")
    medsos = relationship("SocialMedia")
