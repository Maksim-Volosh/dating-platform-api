from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1 import api_v1_router
from app.config import settings
from app.infrastructure.db import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:main_app", 
        host=settings.run.host, 
        port=settings.run.port, 
        reload=settings.run.reload,
    )
