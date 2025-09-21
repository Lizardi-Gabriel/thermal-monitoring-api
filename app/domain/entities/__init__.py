"""
Exportar todas las entidades de dominio
"""
from .user import (
    UserBase, UserCreate, UserUpdate, UserResponse, 
    UserLogin, Token, TokenData
)
from .detection import (
    DetectionBase, DetectionCreate, DetectionUpdate, 
    DetectionResponse, DetectionList, DetectionFilter
)
from .weather_data import (
    WeatherDataBase, WeatherDataCreate, WeatherDataUpdate,
    WeatherDataResponse, WeatherDataList, WeatherDataFilter,
    WeatherSummary
)

# Exportar todas las entidades
__all__ = [
    # User entities
    "UserBase", "UserCreate", "UserUpdate", "UserResponse",
    "UserLogin", "Token", "TokenData",
    
    # Detection entities  
    "DetectionBase", "DetectionCreate", "DetectionUpdate",
    "DetectionResponse", "DetectionList", "DetectionFilter",
    
    # WeatherData entities
    "WeatherDataBase", "WeatherDataCreate", "WeatherDataUpdate", 
    "WeatherDataResponse", "WeatherDataList", "WeatherDataFilter",
    "WeatherSummary"
]