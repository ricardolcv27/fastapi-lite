import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.api import api_router
from app.core.config import Settings
from app.core.middleware import setup_middlewares
from app.db.session import engine

# configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    yield
    logger.info("Shutting down application...")
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

# middlewares
setup_middlewares(app)

# add routers
app.include_router(api_router)


# root endpoint
@app.get("/")
async def root():
    return {
        "message": "Hello",
    }
