from fastapi import FastAPI
from app.config import settings
from app.api.v1 import api_v1_router

app = FastAPI()
app.include_router(api_v1_router, prefix=settings.api.api_prefix)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", 
        host=settings.run.host, 
        port=settings.run.port, 
        reload=settings.run.reload,
    )
