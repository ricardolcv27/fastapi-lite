import logging
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
app = FastAPI()

# middlewares
setup_middlewares(app)

# add routers
app.include_router(api_router)


# startup
@app.on_event("startup")
async def on_startup():
    logger.info("Starting application...")


# shutdown
@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Shutting down application...")
    await engine.dispose()


# root endpoint
@app.get("/")
async def root():
    return {
        "message": "Hello",
    }
