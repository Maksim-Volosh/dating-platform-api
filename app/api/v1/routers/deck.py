
from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.schemas.user import UserResponse
from app.core.containers.deck import get_user_deck_use_case
from app.domain.exceptions import UserNotFoundById, NoCandidatesFound
from app.domain.use_cases import UserDeckUseCase

router = APIRouter(prefix="/decks", tags=["Deck"])

@router.get("/next/{telegram_id}")
async def get_next_user_from_deck(
    telegram_id: int,
    use_case: UserDeckUseCase = Depends(get_user_deck_use_case)
) -> UserResponse:
    try:
        user_entity = await use_case.next(telegram_id)
    except UserNotFoundById:
        raise HTTPException(status_code=404, detail=f"User with telegram_id: {telegram_id} not found")
    except NoCandidatesFound:
        raise HTTPException(status_code=404, detail="No candidates found")
    return UserResponse.model_validate(user_entity, from_attributes=True)