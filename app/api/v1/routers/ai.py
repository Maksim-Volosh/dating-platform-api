from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.v1.schemas.ai import AIProfileAnalizeResponse
from app.core.container import Container
from app.core.dependencies import get_existing_user
from app.core.di import get_container
from app.domain.entities import UserEntity
from app.domain.exceptions import NoCandidatesFound, UserNotFoundById
from app.domain.exceptions.ai import AIUnavailableError

router = APIRouter(prefix="/ai", tags=["AI"])


@router.get("/profile-analize/{telegram_id}")
async def get_ai_analize_for_user(
    telegram_id: int,
    container: Container = Depends(get_container),
) -> AIProfileAnalizeResponse:
    try:
        result = await container.ai_profile_analize_use_case().execute(telegram_id)
    except UserNotFoundById as e:
        raise HTTPException(status_code=404, detail=e.message)
    except AIUnavailableError as e:
        raise HTTPException(status_code=404, detail=e.message)
    return AIProfileAnalizeResponse(response=result)

@router.get("/match-opener/{telegram_id}")
async def generate_match_messages(
    telegram_id: int,
    candidate_id: int = Query(..., description="Who is candidate for match opener"),
    container: Container = Depends(get_container),
) -> AIProfileAnalizeResponse:
    try:
        result = await container.ai_match_opener_use_case().execute(telegram_id, candidate_id)
    except UserNotFoundById as e:
        raise HTTPException(status_code=404, detail=e.message)
    except AIUnavailableError as e:
        raise HTTPException(status_code=404, detail=e.message)
    return AIProfileAnalizeResponse(response=result)
