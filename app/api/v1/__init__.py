from fastapi import APIRouter
    
from . import deck_router, photo_router, user_router

api_v1_router = APIRouter(prefix="/v1")

api_v1_router.include_router(user_router.router, prefix="/users", tags=["User"])
api_v1_router.include_router(photo_router.router, prefix="/users", tags=["User Photos"])
api_v1_router.include_router(deck_router.router, prefix="/decks", tags=["Deck"])