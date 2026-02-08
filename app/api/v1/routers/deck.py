from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.schemas.user import UserDistanceResponse
from app.core.composition.container import Container
from app.api.v1.dependencies.auth import get_existing_user
from app.core.composition.di import get_container
from app.domain.entities import UserEntity
from app.domain.exceptions import NoCandidatesFound, UserNotFoundById

router = APIRouter(prefix="/decks", tags=["Deck"])


@router.post("/next/{telegram_id}")
async def get_next_user_from_deck(
    user: UserEntity = Depends(get_existing_user),
    container: Container = Depends(get_container),
) -> UserDistanceResponse:
    try:
        user_entity = await container.user_deck_use_case().next(user)
    except UserNotFoundById as e:
        raise HTTPException(status_code=404, detail=e.message)
    except NoCandidatesFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    return UserDistanceResponse.model_validate(user_entity, from_attributes=True)
