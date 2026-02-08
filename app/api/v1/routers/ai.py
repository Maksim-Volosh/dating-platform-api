from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.v1.schemas.ai import AIProfileAnalizeResponse
from app.core.composition.container import Container
from app.core.composition.di import get_container
from app.api.v1.dependencies.rate_limit import ai_rate_limit
from app.domain.exceptions import UserNotFoundById
from app.domain.exceptions.ai import AIUnavailableError
from app.core.config import settings

router = APIRouter(prefix="/ai", tags=["AI"])


@router.get(
    "/profile-analize/{telegram_id}",
    dependencies=[
        Depends(
            ai_rate_limit(
                limit=settings.ai_rate_limits.profile_analyze.limit,
                window_sec=settings.ai_rate_limits.profile_analyze.window_sec,
                prefix="ai:profile",
            )
        )
    ],
)
async def get_ai_analize_for_user(
    telegram_id: int,
    container: Container = Depends(get_container),
) -> AIProfileAnalizeResponse:
    try:
        result = await container.ai_profile_analize_use_case().execute(telegram_id)
    except UserNotFoundById as e:
        raise HTTPException(status_code=404, detail=e.message)
    except AIUnavailableError as e:
        raise HTTPException(status_code=503, detail=e.message)
    return AIProfileAnalizeResponse(response=result)


@router.get(
    "/match-opener/{telegram_id}",
    dependencies=[
        Depends(
            ai_rate_limit(
                limit=settings.ai_rate_limits.match_opener.limit,
                window_sec=settings.ai_rate_limits.match_opener.window_sec,
                prefix="ai:opener",
            )
        )
    ],
)
async def generate_match_messages(
    telegram_id: int,
    candidate_id: int = Query(..., description="Who is candidate for match opener"),
    container: Container = Depends(get_container),
) -> AIProfileAnalizeResponse:
    try:
        result = await container.ai_match_opener_use_case().execute(
            telegram_id, candidate_id
        )
    except UserNotFoundById as e:
        raise HTTPException(status_code=404, detail=e.message)
    except AIUnavailableError as e:
        raise HTTPException(status_code=503, detail=e.message)
    return AIProfileAnalizeResponse(response=result)
