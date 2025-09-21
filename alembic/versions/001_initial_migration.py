"""
Migración inicial - Crear tablas users, detections, weather_data

Revision ID: 001
Revises: 
Create Date: 2024-01-15 10:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Información de revisión
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """
    Aplicar migración - Crear todas las tablas
    """
    # Crear tabla users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('hashedPassword', sa.String(length=255), nullable=False),
        sa.Column('fullName', sa.String(length=100), nullable=True),
        sa.Column('isActive', sa.Boolean(), nullable=False, default=True),
        sa.Column('isAdmin', sa.Boolean(), nullable=False, default=False),
        sa.Column('createdAt', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updatedAt', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )
    
    # Crear índices para users
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    
    # Crear tabla detections
    op.create_table(
        'detections',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('detectionType', sa.String(length=50), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('bboxX', sa.Integer(), nullable=True),
        sa.Column('bboxY', sa.Integer(), nullable=True),
        sa.Column('bboxWidth', sa.Integer(), nullable=True),
        sa.Column('bboxHeight', sa.Integer(), nullable=True),
        sa.Column('imagePath', sa.String(length=255), nullable=True),
        sa.Column('cameraId', sa.String(length=50), nullable=True),
        sa.Column('processed', sa.Boolean(), nullable=False, default=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=True),
        sa.Column('createdAt', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Crear índices para detections
    op.create_index('ix_detections_id', 'detections', ['id'], unique=False)
    op.create_index('ix_detections_detectionType', 'detections', ['detectionType'], unique=False)
    op.create_index('ix_detections_cameraId', 'detections', ['cameraId'], unique=False)
    op.create_index('ix_detections_processed', 'detections', ['processed'], unique=False)
    op.create_index('ix_detections_createdAt', 'detections', ['createdAt'], unique=False)
    
    # Crear tabla weather_data
    op.create_table(
        'weather_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('temperature', sa.Float(), nullable=True),
        sa.Column('humidity', sa.Float(), nullable=True),
        sa.Column('windSpeed', sa.Float(), nullable=True),
        sa.Column('windDirection', sa.Integer(), nullable=True),
        sa.Column('pressure', sa.Float(), nullable=True),
        sa.Column('rainfall', sa.Float(), nullable=True),
        sa.Column('sensorId', sa.String(length=50), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=True),
        sa.Column('createdAt', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Crear índices para weather_data
    op.create_index('ix_weather_data_id', 'weather_data', ['id'], unique=False)
    op.create_index('ix_weather_data_sensorId', 'weather_data', ['sensorId'], unique=False)
    op.create_index('ix_weather_data_createdAt', 'weather_data', ['createdAt'], unique=False)
    
    # Insertar usuario administrador por defecto
    op.execute("""
        INSERT INTO users (username, email, hashedPassword, fullName, isAdmin, isActive) 
        VALUES (
            'admin', 
            'admin@thermal-monitoring.com', 
            '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3jgdpVjHxm', 
            'System Administrator', 
            true, 
            true
        )
    """)
    # Nota: Password hasheado es 'admin123' - CAMBIAR EN PRODUCCIÓN

def downgrade() -> None:
    """
    Revertir migración - Eliminar todas las tablas
    """
    # Eliminar tablas en orden inverso
    op.drop_table('weather_data')
    op.drop_table('detections') 
    op.drop_table('users')