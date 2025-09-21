"""
Exportar todos los modelos SQLAlchemy
"""
from .user_model import UserModel
from .detection_model import DetectionModel
from .weather_model import WeatherModel

# Exportar modelos para que Alembic los detecte
__all__ = [
    "UserModel",
    "DetectionModel", 
    "WeatherModel"
]