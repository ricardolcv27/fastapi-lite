# FastAPI Template

Template para arrancar un backend con FastAPI, PostgreSQL con SQLAlchemy y Alembic.

## Características

- **FastAPI** - Framework web moderno y rápido
- **PostgreSQL** - Base de datos relacional
- **SQLAlchemy (async)** - ORM con soporte asíncrono
- **Alembic** - Migraciones de base de datos
- **Docker + Docker Compose** - Desarrollo containerizado
- **Middlewares** - CORS y logging configurados
- **Pydantic** - Validación automática de datos
- **pytest** - Tests unitarios con SQLite en memoria

## Estructura del proyecto

```
python_template/
├── app/
│   ├── main.py              # Punto de entrada + middlewares
│   ├── core/
│   │   ├── config.py        # Configuración (env vars)
│   │   └── middleware.py    # Middlewares CORS y logging
│   ├── db/
│   │   ├── base.py          # Base de SQLAlchemy
│   │   └── session.py       # Engine async + get_session
│   ├── models/              # Modelos SQLAlchemy (tablas)
│   │   └── user.py
│   ├── schemas/             # Pydantic schemas (DTOs)
│   │   └── user.py
│   ├── crud/                # Lógica de acceso a datos
│   │   └── user.py
│   └── api/
│       ├── api.py           # Router principal
│       └── endpoints/
│           └── users.py     # Endpoints de usuarios
├── alembic/                 # Migraciones
│   ├── versions/            # Archivos de migración
│   └── env.py               # Configuración de Alembic
├── tests/                   # Tests con SQLite en memoria
│   ├── conftest.py          # Fixtures y configuración
│   └── test_users.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini              # Configuración de Alembic
├── Makefile                 # Comandos útiles
└── .env.example
```

## Inicio rápido

### 1. Clonar y configurar

```bash
# Copiar variables de entorno
cp .env.example .env

# Editar .env si es necesario (opcional)
```

### 2. Levantar con Docker Compose (recomendado)

```bash
docker-compose up --build
```

La API estará en:
- **API**: http://localhost:8000

### 3. Desarrollo local (sin Docker)

```bash
# Crear virtualenv
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
make install
# O manualmente: pip install -r requirements.txt

# Levantar servidor
make dev
# O manualmente: uvicorn app.main:app --reload
```

## Migraciones de base de datos con Alembic

### Usando Makefile (recomendado)

```bash
# Crear migración
make migrate MSG="Add phone to users"

# Aplicar migraciones
make push

# Revertir última migración
make rollback

# Ver historial
make history
```

### Ejemplo: Agregar campo a User

1. **Editar el modelo** (`app/models/user.py`):
   ```python
   class User(Base):
       __tablename__ = "users"
       id = Column(Integer, primary_key=True, index=True)
       email = Column(String, unique=True, index=True)
       full_name = Column(String, nullable=True)
       phone = Column(String, nullable=True)  # ← NUEVO
   ```

2. **Crear migración**:
   ```bash
   make migrate MSG="Add phone to users"
   ```

3. **Aplicar migración**:
   ```bash
   make push
   ```

## Comandos útiles (Makefile)

```bash
make help       # Ver todos los comandos disponibles
make install    # Instalar dependencias
make dev        # Iniciar servidor en desarrollo
make up         # Levantar Docker Compose
make down       # Detener Docker Compose
make test       # Ejecutar tests
make lint       # Ejecutar linters (flake8 + black)
make shell      # Shell en contenedor Docker
```

## Middlewares configurados

### 1. CORS
Actualmente permite todas las origins (`*`). Para restringir, editar `app/core/middleware.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Cambiar aquí
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### 2. Logging
Logea todas las peticiones HTTP

## Testing

Los tests usan SQLite en memoria en lugar de PostgreSQL para mayor velocidad y sin dependencias externas.

```bash
# Ejecutar todos los tests
make test

# O directamente con pytest
pytest tests/ -v

# Con coverage
pytest tests/ --cov=app
```

### Estructura de tests

- `tests/conftest.py`: Configuración de fixtures (BD en memoria, cliente HTTP)
- `tests/test_users.py`: Tests de endpoints de usuarios

Los tests son completamente independientes y cada uno usa su propia base de datos limpia.

## Variables de entorno

Copiar `.env.example` a `.env` y ajustar:

```bash
#db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_DB=postgres
DATABASE_HOST=db#localhost si no usas docker
DATABASE_PORT=5432
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/postgres

#app
PORT=8000
HOST=0.0.0.0
PUBLIC_URL=http://localhost:8000
```
