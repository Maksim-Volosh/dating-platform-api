from fastapi import APIRouter

from .routers import deck, like, photo, swipe, user

api_v1_router = APIRouter(prefix="/v1")
router_list = [user, photo, deck, swipe, like]

for router in router_list:
    api_v1_router.include_router(router.router)