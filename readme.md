# Thermal Monitoring API

Sistema de monitoreo de zonas para no fumadores

## Descripción

API REST desarrollada en FastAPI que procesa datos

## Stack Tecnológico

- **Framework**: FastAPI (Python)
- **Base de Datos**: MySQL 8.0
- **ORM**: SQLAlchemy con soporte asíncrono
- **Migraciones**: Alembic
- **Contenedores**: Docker + Docker Compose
- **Validación**: Pydantic

## Prerrequisitos

- Docker y Docker Compose instalados
- Git para clonar el repositorio

## Instalación y Primera Ejecución

### 1. Clonar repositorio

```bash
git clone https://github.com/tu-usuario/thermal-monitoring-api.git
cd thermal-monitoring-api
```

### 2. Configurar variables de entorno

```bash
# El archivo .env ya está configurado para desarrollo
# Revisar configuración si es necesario
cat .env
```

### 3. Ejecutar por primera vez

```bash
# Construir y levantar todos los servicios
docker-compose up --build

# En otra terminal, aplicar migraciones de base de datos (SOLO LA PRIMERA VEZ)
docker-compose exec api alembic upgrade head
```

### 4. Verificar instalación

- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Base de datos (Adminer)**: http://localhost:8080
- **Health Check**: http://localhost:8000/health

## Uso Diario (después de la primera instalación)

Para desarrollo normal, solo necesitas:

```bash
# Levantar servicios (los datos persisten automáticamente)
docker-compose up

# Para detener servicios
docker-compose down
```

**Los datos de MySQL se mantienen automáticamente entre reinicios.**

## Gestión de Base de Datos

### Acceder a la base de datos

**Opción 1: Adminer (Interfaz web)**

- URL: http://localhost:8080
- Server: `mysql`
- Username: `thermal_user`
- Password: `thermal_pass123`
- Database: `thermal_monitoring`

**Opción 2: Línea de comandos**

```bash
docker-compose exec mysql mysql -u thermal_user -p thermal_monitoring
# Password: thermal_pass123
```

### Usuario administrador por defecto

El sistema crea automáticamente un usuario administrador:

- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@thermal-monitoring.com`

## Migraciones de Base de Datos

### Aplicar migraciones existentes

```bash
# Ver estado actual de migraciones
docker-compose exec api alembic current

# Aplicar todas las migraciones pendientes
docker-compose exec api alembic upgrade head

# Ver historial de migraciones
docker-compose exec api alembic history
```

### Crear nuevas migraciones (desarrollo)

```bash
# Después de modificar modelos en app/infrastructure/database/models/
# Generar migración automáticamente
docker-compose exec api alembic revision --autogenerate -m "descripcion_del_cambio"

# Aplicar la nueva migración
docker-compose exec api alembic upgrade head
```

### Revertir migraciones

```bash
# Revertir una migración
docker-compose exec api alembic downgrade -1

# Revertir a migración específica
docker-compose exec api alembic downgrade 001
```

## Servicios Docker

| Servicio  | Puerto | Descripción             |
| --------- | ------ | ----------------------- |
| `api`     | 8000   | API FastAPI             |
| `mysql`   | 3306   | Base de datos MySQL     |
| `adminer` | 8080   | Interfaz web para MySQL |

## Troubleshooting

### Error de conexión a base de datos

```bash
# Verificar que MySQL esté corriendo
docker-compose ps

# Ver logs de MySQL
docker-compose logs mysql

# Reiniciar MySQL
docker-compose restart mysql
```

### Recrear base de datos desde cero

```bash
# CUIDADO: Esto elimina todos los datos
docker-compose down -v
docker-compose up --build
docker-compose exec api alembic upgrade head
```

### Verificar estado de migraciones

```bash
# Ver migración actual
docker-compose exec api alembic current

# Ver todas las migraciones disponibles
docker-compose exec api alembic history

# Verificar que las tablas existan
docker-compose exec mysql mysql -u thermal_user -p -e "SHOW TABLES;" thermal_monitoring
```
