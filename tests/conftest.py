import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db.base import Base
from app.db.session import get_session

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL, 
    echo=False,
    connect_args={"check_same_thread": False}
)

test_async_session = sessionmaker(
    test_engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)


async def override_get_session():
    # override de la sesion de base de datos para tests
    async with test_async_session() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def cleanup_engine():
    yield  #espera a que todos los tests terminen
    #cerrar el engine al finalizar todos los tests
    import asyncio
    asyncio.run(test_engine.dispose())


@pytest_asyncio.fixture(scope="function")
async def db_session():
    #before
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # provide session
    async with test_async_session() as session:
        yield session
    
    #after
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    #uso la session de la db de sqlite en memoria para test
    app.dependency_overrides[get_session] = override_get_session
    
    #crea cliente http para test
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        yield ac
    
    # limpiar overrides
    app.dependency_overrides.clear()
