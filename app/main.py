import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1 import api_v1_router
from app.core.config import settings
from app.core.dependencies import verify_bot_key
from app.infrastructure.db import db_helper
from app.infrastructure.models import Base
from app.infrastructure.redis import redis_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize
    
    yield # ---------
    
    # Cleanup
    await db_helper.dispose()
    await redis_helper.dispose()

main_app = FastAPI(
    lifespan=lifespan,
    title=settings.details.title,
    description=settings.details.description,
    dependencies=[Depends(verify_bot_key)],
)
main_app.include_router(api_v1_router, prefix=settings.api.prefix)

os.makedirs(settings.static.directory, exist_ok=True)
main_app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:main_app", 
        host=settings.run.host, 
        port=settings.run.port, 
        reload=settings.run.reload,
    )
