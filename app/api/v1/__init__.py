from fastapi import APIRouter

from .routers import deck, inbox, photo, swipe, user, ai

api_v1_router = APIRouter(prefix="/v1")
router_list = [user, photo, deck, swipe, inbox, ai]

for router in router_list:
    api_v1_router.include_router(router.router)
