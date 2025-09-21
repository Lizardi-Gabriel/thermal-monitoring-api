"""
Configuración de conexión a base de datos MySQL con SQLAlchemy asíncrono
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada en variables de entorno")

# Crear engine asíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=True if os.getenv("DEBUG", "false").lower() == "true" else False,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Crear session maker asíncrono
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class para todos los modelos
class Base(DeclarativeBase):
    pass

# Dependency para obtener sesión de base de datos
async def getDbSession():
    """
    Dependency para inyectar sesión de base de datos en endpoints FastAPI
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Función para verificar conexión
async def checkDatabaseConnection():
    """
    Verificar que la conexión a base de datos esté funcionando
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
            return True
    except Exception as e:
        print(f"Error de conexión a base de datos: {e}")
        return False

# Función para crear todas las tablas
async def createTables():
    """
    Crear todas las tablas en la base de datos
    Solo para desarrollo, en producción usar Alembic
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)