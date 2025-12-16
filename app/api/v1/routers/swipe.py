from fastapi import APIRouter, Depends

from app.api.v1.schemas.swipe import (SwipeRequest,
                                      SwipeResponse)
from app.core.containers.swipe import (get_swipe_user_use_case)
from app.domain.entities import SwipeEntity
from app.domain.use_cases import SwipeUserUseCase

router = APIRouter(prefix="/swipes", tags=["Swipe"])

@router.post("/", status_code=201)
async def swipe_user(
    swipe: SwipeRequest,
    use_case: SwipeUserUseCase = Depends(get_swipe_user_use_case)
) -> SwipeResponse:
    swipe_entity = SwipeEntity(
        liker_id=swipe.liker_id,
        liked_id=swipe.liked_id,
        decision=swipe.decision
    )
    swipe_entity = await use_case.execute(swipe_entity)
    return SwipeResponse.model_validate(swipe_entity, from_attributes=True)