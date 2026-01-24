from fastapi import APIRouter, Depends

from app.api.v1.schemas.swipe import SwipeRequest, SwipeResponse
from app.core.container import Container
from app.core.di import get_container
from app.domain.entities import SwipeEntity

router = APIRouter(prefix="/swipes", tags=["Swipe"])

@router.post("/", status_code=201)
async def swipe_user(
    swipe: SwipeRequest,
    container: Container = Depends(get_container)
) -> SwipeResponse:
    swipe_entity = SwipeEntity(
        liker_id=swipe.liker_id,
        liked_id=swipe.liked_id,
        decision=swipe.decision
    )
    swipe_entity = await container.swipe_user_use_case().execute(swipe_entity)
    return SwipeResponse.model_validate(swipe_entity, from_attributes=True)