from fastapi import APIRouter
from . import main_router

api_v1_router = APIRouter(prefix="/v1")

api_v1_router.include_router(main_router.router, tags=["Root"])