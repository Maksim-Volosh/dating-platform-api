import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1 import api_v1_router
from app.config import settings
from app.infrastructure.db import db_helper
from app.infrastructure.models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    os.makedirs(settings.static.directory, exist_ok=True)
    # Initialize
    yield
    # Cleanup
    await db_helper.dispose()

main_app = FastAPI(
    lifespan=lifespan,
    title="Dating Platform API",
    description="API for the Dating Platform",
)
main_app.include_router(api_v1_router, prefix=settings.api.prefix)


main_app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:main_app", 
        host=settings.run.host, 
        port=settings.run.port, 
        reload=settings.run.reload,
    )
