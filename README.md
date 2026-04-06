# FastAPI Template

Backend template with FastAPI, PostgreSQL, SQLAlchemy (async) and Alembic.

## Stack

- FastAPI
- PostgreSQL + SQLAlchemy async + Alembic
- Docker + Docker Compose
- pytest (SQLite in-memory)

## Project structure

```
app/
├── main.py
├── core/
│   ├── config.py          # env vars
│   └── middleware.py      # CORS, logging
├── db/
│   ├── base.py
│   └── session.py
├── models/                # SQLAlchemy models
├── schemas/               # Pydantic DTOs
├── repositories/
│   ├── interfaces/        # Abstract interfaces
│   └── user_repository.py # SQLAlchemy implementation
├── services/              # Business logic
├── api/
│   ├── api.py
│   └── endpoints/
├── dependencies.py        # DI wiring
tests/
├── conftest.py
└── test_users.py
```

## Quickstart

```bash
cp .env.example .env
docker-compose up --build
```

API available at `http://localhost:8000`.

## Local development (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Migrations

```bash
make migrate MSG="description"   # create migration
make push                        # apply migrations
make rollback                    # revert last migration
make history                     # show history
```

## Tests

```bash
pytest tests/ -v
```

Each test runs against its own isolated SQLite in-memory database.

## Environment variables

```bash
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_DB=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/postgres

PORT=8000
HOST=0.0.0.0
PUBLIC_URL=http://localhost:8000
```
