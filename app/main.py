"""
Sistema de monitoreo térmico - FastAPI Server
Iteración 1: Endpoints básicos con datos simulados
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uvicorn
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración desde variables de entorno
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
PROJECT_NAME = os.getenv("PROJECT_NAME", "Thermal Monitoring API")
VERSION = os.getenv("VERSION", "1.0.0")
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
CORS_ORIGINS = ["*"]  # En iteraciones futuras lo leeremos de .env

# Configurar aplicación FastAPI
app = FastAPI(
    title=PROJECT_NAME,
    description="Sistema de monitoreo inteligente con cámaras térmicas y sensores meteorológicos",
    version=VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic para validación de datos
class DetectionData(BaseModel):
    detectionType: str
    confidence: float
    bboxX: Optional[int] = None
    bboxY: Optional[int] = None
    bboxWidth: Optional[int] = None
    bboxHeight: Optional[int] = None
    cameraId: Optional[str] = None
    timestamp: Optional[str] = None

class WeatherData(BaseModel):
    temperature: float
    humidity: float
    windSpeed: float
    windDirection: Optional[int] = None
    pressure: Optional[float] = None
    sensorId: Optional[str] = None
    timestamp: Optional[str] = None

class CorrelationResult(BaseModel):
    riskLevel: str
    confidence: float
    factors: dict
    recommendation: str

# Endpoint raíz - Health check
@app.get("/")
async def readRoot():
    """Verificar que la API esté funcionando correctamente"""
    return {
        "message": "Thermal Monitoring API funcionando correctamente",
        "version": VERSION,
        "environment": ENVIRONMENT,
        "status": "online",
        "docs": f"http://localhost:{API_PORT}/docs"
    }

@app.get("/health")
async def healthCheck():
    """Endpoint de salud del sistema"""
    return {
        "status": "healthy",
        "service": "thermal-monitoring-api",
        "timestamp": datetime.now().isoformat(),
        "database": "not_connected",
        "iteration": "1"
    }

# Endpoint de prueba para estructura API
@app.get("/api/v1/test")
async def testEndpoint():
    """Verificar estructura de API v1"""
    return {
        "message": "API v1 funcionando correctamente",
        "availableEndpoints": [
            "/api/v1/detections",
            "/api/v1/weather",
            "/api/v1/analysis/correlation"
        ],
        "iteration": "1"
    }

# Recibir detecciones del módulo de visión
@app.post("/api/v1/detections")
async def receiveDetection(detectionData: DetectionData):
    """
    Recibir detecciones del módulo de visión por computadora
    En esta iteración retorna respuesta simulada
    """
    return {
        "status": "received",
        "message": "Detección procesada correctamente",
        "detectionId": "det_001",
        "data": {
            "detectionType": detectionData.detectionType,
            "confidence": detectionData.confidence,
            "cameraId": detectionData.cameraId or "THERMAL_CAM_001",
            "processedAt": datetime.now().isoformat()
        },
        "nextAction": "correlation_analysis",
        "iteration": "1"
    }

# Recibir datos meteorológicos
@app.post("/api/v1/weather")
async def receiveWeather(weatherData: WeatherData):
    """
    Recibir datos meteorológicos cada 5 minutos
    En esta iteración retorna respuesta simulada
    """
    return {
        "status": "received",
        "message": "Datos meteorológicos procesados correctamente",
        "weatherId": "weather_001",
        "data": {
            "temperature": weatherData.temperature,
            "humidity": weatherData.humidity,
            "windSpeed": weatherData.windSpeed,
            "sensorId": weatherData.sensorId or "DAVIS_V3_001",
            "processedAt": datetime.now().isoformat()
        },
        "nextUpdate": "in_5_minutes",
        "iteration": "1"
    }

# Motor principal - Correlación de datos
@app.get("/api/v1/analysis/correlation", response_model=CorrelationResult)
async def getCorrelation():
    """
    Motor principal de correlación de datos
    En esta iteración retorna análisis simulado
    """
    return CorrelationResult(
        riskLevel="medium",
        confidence=0.85,
        factors={
            "thermalDetection": True,
            "weatherConditions": "favorable_for_fire",
            "windSpeed": "15_kmh",
            "humidity": "25_percent",
            "temperature": "28_celsius"
        },
        recommendation="Aumentar vigilancia en sector detectado"
    )

# Obtener lista de detecciones
@app.get("/api/v1/detections")
async def getDetections():
    """
    Obtener lista de detecciones registradas
    En esta iteración retorna datos simulados
    """
    simulatedDetections = [
        {
            "id": "det_001",
            "detectionType": "fire",
            "confidence": 0.92,
            "cameraId": "THERMAL_CAM_001",
            "timestamp": "2024-01-15T10:30:00Z",
            "processed": True
        },
        {
            "id": "det_002", 
            "detectionType": "smoke",
            "confidence": 0.78,
            "cameraId": "THERMAL_CAM_001",
            "timestamp": "2024-01-15T10:25:00Z",
            "processed": True
        }
    ]
    
    return {
        "detections": simulatedDetections,
        "totalCount": len(simulatedDetections),
        "iteration": "1"
    }

# Obtener datos meteorológicos
@app.get("/api/v1/weather")
async def getWeatherData():
    """
    Obtener datos meteorológicos actuales
    En esta iteración retorna datos simulados
    """
    simulatedWeatherData = [
        {
            "id": "weather_001",
            "temperature": 25.5,
            "humidity": 45.2,
            "windSpeed": 12.3,
            "windDirection": 180,
            "sensorId": "DAVIS_V3_001",
            "timestamp": "2024-01-15T10:30:00Z"
        },
        {
            "id": "weather_002",
            "temperature": 26.8,
            "humidity": 42.1,
            "windSpeed": 15.7,
            "windDirection": 165,
            "sensorId": "DAVIS_V3_001",
            "timestamp": "2024-01-15T10:25:00Z"
        }
    ]
    
    return {
        "weatherData": simulatedWeatherData,
        "totalCount": len(simulatedWeatherData),
        "iteration": "1"
    }

# Ejecutar servidor si se ejecuta directamente
if __name__ == "__main__":
    print(f"Iniciando {PROJECT_NAME} - Iteración 1")
    print(f"Ambiente: {ENVIRONMENT}")
    print(f"Debug: {DEBUG}")
    print(f"Documentación disponible en: http://{API_HOST}:{API_PORT}/docs")
    
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=DEBUG,
        log_level=LOG_LEVEL.lower()
    )