"""
Configuración de entorno para Alembic
"""
import asyncio
import os
import sys
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from dotenv import load_dotenv

# Agregar directorio padre al path para importar app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cargar variables de entorno
load_dotenv()

# Importar Base y modelos para que Alembic los detecte
from app.infrastructure.database.connection import Base
from app.infrastructure.database.models import UserModel, DetectionModel, WeatherModel

# Configuración de Alembic
config = context.config

# Configurar logging si existe archivo de configuración
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata para autogenerar migraciones
target_metadata = Base.metadata

# URL de base de datos desde variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

def get_url():
    """Obtener URL de base de datos"""
    return DATABASE_URL or config.get_main_option("sqlalchemy.url")

def run_migrations_offline() -> None:
    """
    Ejecutar migraciones en modo offline
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    """
    Ejecutar migraciones con conexión proporcionada
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """
    Ejecutar migraciones en modo asíncrono
    """
    connectable = create_async_engine(
        get_url(),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """
    Ejecutar migraciones en modo online
    """
    asyncio.run(run_async_migrations())

# Determinar modo de ejecución
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()