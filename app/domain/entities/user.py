"""
Entidades Pydantic para User - Validación de API
"""
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Campos base compartidos entre modelos de User"""
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único")
    email: str = Field(..., description="Dirección de correo electrónico")
    fullName: Optional[str] = Field(None, max_length=100, description="Nombre completo del usuario")

class UserCreate(UserBase):
    """Modelo para crear nuevo usuario"""
    password: str = Field(..., min_length=6, max_length=100, description="Contraseña del usuario")
    
    @validator('username')
    def validateUsername(cls, v):
        if not v.isalnum():
            raise ValueError('username solo puede contener letras y números')
        return v.lower()
    
    @validator('password')
    def validatePassword(cls, v):
        if len(v) < 6:
            raise ValueError('password debe tener al menos 6 caracteres')
        return v

class UserUpdate(BaseModel):
    """Modelo para actualizar usuario existente"""
    email: Optional[str] = Field(None, description="Nueva dirección de correo")
    fullName: Optional[str] = Field(None, max_length=100, description="Nuevo nombre completo")
    isActive: Optional[bool] = Field(None, description="Estado activo del usuario")

class UserResponse(UserBase):
    """Modelo de respuesta con información del usuario"""
    id: int = Field(..., description="ID único del usuario")
    isActive: bool = Field(..., description="Si el usuario está activo")
    isAdmin: bool = Field(..., description="Si el usuario es administrador")
    createdAt: datetime = Field(..., description="Fecha de creación")
    updatedAt: datetime = Field(..., description="Fecha de última actualización")
    
    class Config:
        from_attributes = True
        orm_mode = True

class UserLogin(BaseModel):
    """Modelo para login de usuario"""
    username: str = Field(..., description="Nombre de usuario")
    password: str = Field(..., description="Contraseña")

class Token(BaseModel):
    """Modelo de respuesta para token JWT"""
    accessToken: str = Field(..., description="Token de acceso JWT")
    tokenType: str = Field(default="bearer", description="Tipo de token")
    expiresIn: int = Field(..., description="Tiempo de expiración en segundos")

class TokenData(BaseModel):
    """Datos contenidos en el token JWT"""
    username: Optional[str] = None
    userId: Optional[int] = None