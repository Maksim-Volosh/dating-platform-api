from fastapi import Depends, HTTPException, Request

from app.core.composition.container import Container
from app.core.composition.di import get_container
from app.domain.exceptions import RateLimitTooManyRequests


def ai_rate_limit(
    *,
    limit: int,
    window_sec: int,
    prefix: str,
):
    async def dependency(
        request: Request,
        container: Container = Depends(get_container),
    ) -> None:
        telegram_id = request.path_params["telegram_id"]
        
        key = f"rl:{prefix}:{telegram_id}"

        try:
            await container.get_rate_limiter().hit(key, limit=limit, window_sec=window_sec)
        except RateLimitTooManyRequests:
            raise HTTPException(
                status_code=429,
                detail="Too many requests",
            )
    return dependency
