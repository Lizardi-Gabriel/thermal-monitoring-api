"""
Modelo SQLAlchemy para tabla detections
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.infrastructure.database.connection import Base

class DetectionModel(Base):
    __tablename__ = "detections"
    
    id = Column(Integer, primary_key=True, index=True)
    detectionType = Column(String(50), nullable=False, index=True)
    confidence = Column(Float, nullable=False)
    
    # Coordenadas del bounding box
    bboxX = Column(Integer, nullable=True)
    bboxY = Column(Integer, nullable=True) 
    bboxWidth = Column(Integer, nullable=True)
    bboxHeight = Column(Integer, nullable=True)
    
    # Metadatos
    imagePath = Column(String(255), nullable=True)
    cameraId = Column(String(50), nullable=True, index=True)
    processed = Column(Boolean, default=False, nullable=False, index=True)
    
    # Timestamps
    timestamp = Column(DateTime(timezone=True), nullable=True)
    createdAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    def __repr__(self):
        return f"<DetectionModel(id={self.id}, type='{self.detectionType}', confidence={self.confidence})>"