from fastapi import Depends
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.container import Container
from app.infrastructure.db import db_helper
from app.infrastructure.redis import redis_helper


async def get_container(
    session: AsyncSession = Depends(db_helper.session_getter),
    redis: Redis = Depends(redis_helper.get_client),
) -> Container:
    return Container(session=session, redis=redis)
