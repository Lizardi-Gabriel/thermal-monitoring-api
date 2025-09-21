"""
Entidades Pydantic para Detection - Validación de API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class DetectionBase(BaseModel):
    """Campos base compartidos entre modelos de Detection"""
    detectionType: str = Field(..., description="Tipo de detección")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Nivel de confianza entre 0.0 y 1.0")
    cameraId: Optional[str] = Field(None, description="Identificador de la cámara")

class DetectionCreate(DetectionBase):
    """Modelo para crear nueva detección (POST desde módulo visión)"""
    bboxX: Optional[int] = Field(None, ge=0, description="Coordenada X del bounding box")
    bboxY: Optional[int] = Field(None, ge=0, description="Coordenada Y del bounding box") 
    bboxWidth: Optional[int] = Field(None, ge=1, description="Ancho del bounding box")
    bboxHeight: Optional[int] = Field(None, ge=1, description="Alto del bounding box")
    imagePath: Optional[str] = Field(None, description="Ruta de la imagen capturada")
    timestamp: Optional[datetime] = Field(None, description="Timestamp de la detección")
    
    @validator('detectionType')
    def validateDetectionType(cls, v):
        allowedTypes = ['fire', 'smoke', 'person', 'vehicle', 'animal']
        if v.lower() not in allowedTypes:
            raise ValueError(f'detectionType debe ser uno de: {allowedTypes}')
        return v.lower()
    
    @validator('confidence')
    def validateConfidence(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('confidence debe estar entre 0.0 y 1.0')
        return round(v, 4)  # Redondear a 4 decimales

class DetectionUpdate(BaseModel):
    """Modelo para actualizar detección existente"""
    processed: Optional[bool] = Field(None, description="Si la detección fue procesada")
    imagePath: Optional[str] = Field(None, description="Nueva ruta de imagen")

class DetectionResponse(DetectionBase):
    """Modelo de respuesta con información completa de detección"""
    id: int = Field(..., description="ID único de la detección")
    bboxX: Optional[int] = Field(None, description="Coordenada X del bounding box")
    bboxY: Optional[int] = Field(None, description="Coordenada Y del bounding box")
    bboxWidth: Optional[int] = Field(None, description="Ancho del bounding box") 
    bboxHeight: Optional[int] = Field(None, description="Alto del bounding box")
    imagePath: Optional[str] = Field(None, description="Ruta de la imagen")
    processed: bool = Field(..., description="Si fue procesada por motor de correlación")
    timestamp: Optional[datetime] = Field(None, description="Timestamp original")
    createdAt: datetime = Field(..., description="Fecha de registro en sistema")
    
    class Config:
        from_attributes = True
        orm_mode = True

class DetectionList(BaseModel):
    """Modelo para lista de detecciones con paginación"""
    detections: List[DetectionResponse] = Field(..., description="Lista de detecciones")
    totalCount: int = Field(..., description="Total de detecciones")
    page: int = Field(default=1, description="Página actual")
    pageSize: int = Field(default=10, description="Elementos por página")
    
class DetectionFilter(BaseModel):
    """Modelo para filtros de búsqueda de detecciones"""
    detectionType: Optional[str] = Field(None, description="Filtrar por tipo")
    cameraId: Optional[str] = Field(None, description="Filtrar por cámara")
    processed: Optional[bool] = Field(None, description="Filtrar por estado procesado")
    minConfidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confianza mínima")
    startDate: Optional[datetime] = Field(None, description="Fecha inicio")
    endDate: Optional[datetime] = Field(None, description="Fecha fin")