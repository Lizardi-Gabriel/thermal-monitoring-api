"""
Entidades Pydantic para WeatherData - Validación de API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class WeatherDataBase(BaseModel):
    """Campos base compartidos entre modelos de WeatherData"""
    temperature: Optional[float] = Field(None, description="Temperatura en grados Celsius")
    humidity: Optional[float] = Field(None, ge=0.0, le=100.0, description="Humedad relativa en porcentaje")
    windSpeed: Optional[float] = Field(None, ge=0.0, description="Velocidad del viento en km/h")
    sensorId: Optional[str] = Field(None, description="Identificador del sensor meteorológico")

class WeatherDataCreate(WeatherDataBase):
    """Modelo para crear nuevo registro meteorológico (POST cada 5 min)"""
    windDirection: Optional[int] = Field(None, ge=0, le=360, description="Dirección del viento en grados")
    pressure: Optional[float] = Field(None, ge=800.0, le=1200.0, description="Presión atmosférica en hPa")
    rainfall: Optional[float] = Field(None, ge=0.0, description="Precipitación en mm")
    timestamp: Optional[datetime] = Field(None, description="Timestamp de la lectura")
    
    @validator('temperature')
    def validateTemperature(cls, v):
        if v is not None and not -50.0 <= v <= 70.0:
            raise ValueError('temperature debe estar entre -50°C y 70°C')
        return round(v, 2) if v is not None else v
    
    @validator('humidity') 
    def validateHumidity(cls, v):
        if v is not None and not 0.0 <= v <= 100.0:
            raise ValueError('humidity debe estar entre 0% y 100%')
        return round(v, 2) if v is not None else v
    
    @validator('windSpeed')
    def validateWindSpeed(cls, v):
        if v is not None and v < 0.0:
            raise ValueError('windSpeed no puede ser negativa')
        return round(v, 2) if v is not None else v
    
    @validator('pressure')
    def validatePressure(cls, v):
        if v is not None and not 800.0 <= v <= 1200.0:
            raise ValueError('pressure debe estar entre 800 hPa y 1200 hPa')
        return round(v, 2) if v is not None else v

class WeatherDataUpdate(BaseModel):
    """Modelo para actualizar registro meteorológico existente"""
    temperature: Optional[float] = Field(None, description="Nueva temperatura")
    humidity: Optional[float] = Field(None, ge=0.0, le=100.0, description="Nueva humedad")
    windSpeed: Optional[float] = Field(None, ge=0.0, description="Nueva velocidad viento")

class WeatherDataResponse(WeatherDataBase):
    """Modelo de respuesta con información completa meteorológica"""
    id: int = Field(..., description="ID único del registro")
    windDirection: Optional[int] = Field(None, description="Dirección del viento en grados")
    pressure: Optional[float] = Field(None, description="Presión atmosférica en hPa")
    rainfall: Optional[float] = Field(None, description="Precipitación en mm")
    timestamp: Optional[datetime] = Field(None, description="Timestamp original")
    createdAt: datetime = Field(..., description="Fecha de registro en sistema")
    
    class Config:
        from_attributes = True
        orm_mode = True

class WeatherDataList(BaseModel):
    """Modelo para lista de datos meteorológicos con paginación"""
    weatherData: List[WeatherDataResponse] = Field(..., description="Lista de registros meteorológicos")
    totalCount: int = Field(..., description="Total de registros")
    page: int = Field(default=1, description="Página actual")
    pageSize: int = Field(default=10, description="Elementos por página")

class WeatherDataFilter(BaseModel):
    """Modelo para filtros de búsqueda de datos meteorológicos"""
    sensorId: Optional[str] = Field(None, description="Filtrar por sensor")
    minTemperature: Optional[float] = Field(None, description="Temperatura mínima")
    maxTemperature: Optional[float] = Field(None, description="Temperatura máxima")
    minHumidity: Optional[float] = Field(None, description="Humedad mínima")
    maxHumidity: Optional[float] = Field(None, description="Humedad máxima")
    startDate: Optional[datetime] = Field(None, description="Fecha inicio")
    endDate: Optional[datetime] = Field(None, description="Fecha fin")

class WeatherSummary(BaseModel):
    """Resumen estadístico de datos meteorológicos"""
    avgTemperature: Optional[float] = Field(None, description="Temperatura promedio")
    maxTemperature: Optional[float] = Field(None, description="Temperatura máxima")
    minTemperature: Optional[float] = Field(None, description="Temperatura mínima")
    avgHumidity: Optional[float] = Field(None, description="Humedad promedio")
    avgWindSpeed: Optional[float] = Field(None, description="Velocidad promedio del viento")
    totalRainfall: Optional[float] = Field(None, description="Precipitación total")
    recordCount: int = Field(..., description="Número de registros analizados")
    periodStart: datetime = Field(..., description="Inicio del período")
    periodEnd: datetime = Field(..., description="Fin del período")