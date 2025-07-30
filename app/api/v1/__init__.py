from fastapi import APIRouter

from .routers import deck, photo, user, swipe

api_v1_router = APIRouter(prefix="/v1")
router_list = [user, photo, deck, swipe]

for router in router_list:
    api_v1_router.include_router(router.router)