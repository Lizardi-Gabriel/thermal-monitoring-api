"""
Modelo SQLAlchemy para tabla users
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.infrastructure.database.connection import Base

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashedPassword = Column(String(255), nullable=False)
    fullName = Column(String(100), nullable=True)
    isActive = Column(Boolean, default=True, nullable=False)
    isAdmin = Column(Boolean, default=False, nullable=False)
    
    # Timestamps automáticos
    createdAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<UserModel(id={self.id}, username='{self.username}', email='{self.email}')>"