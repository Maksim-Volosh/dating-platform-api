from fastapi import APIRouter
    
from .endpoints import deck_router, photo_router, user_router

api_v1_router = APIRouter(prefix="/v1")
router_list = [user_router, photo_router, deck_router]

for router in router_list:
    api_v1_router.include_router(router.router)