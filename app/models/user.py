from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.base_class import Base

class User(Base):
    __tablename__ = "tb_m_user"

    user_id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("tb_m_role.role_id"), nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    fullname = Column(String, index=True)
    phone = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    user_inf = Column(String, nullable=True)
    user_picture_path = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    reset_token = Column(String, nullable=True)
    token_expiry_dt = Column(DateTime(timezone=True), nullable=True)
    
    created_dt = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=True)
    changed_dt = Column(DateTime(timezone=True), onupdate=func.now())
    changed_by = Column(String, nullable=True)
