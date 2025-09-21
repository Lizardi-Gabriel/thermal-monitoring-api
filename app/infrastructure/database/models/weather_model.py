"""
Modelo SQLAlchemy para tabla weather_data
"""
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.infrastructure.database.connection import Base

class WeatherModel(Base):
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos meteorológicos principales
    temperature = Column(Float, nullable=True)  # Celsius
    humidity = Column(Float, nullable=True)     # Porcentaje
    windSpeed = Column(Float, nullable=True)    # km/h
    windDirection = Column(Integer, nullable=True)  # Grados 0-360
    pressure = Column(Float, nullable=True)     # hPa
    rainfall = Column(Float, nullable=True)     # mm
    
    # Metadatos
    sensorId = Column(String(50), nullable=True, index=True)
    
    # Timestamps
    timestamp = Column(DateTime(timezone=True), nullable=True)
    createdAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    def __repr__(self):
        return f"<WeatherModel(id={self.id}, temp={self.temperature}, humidity={self.humidity})>"