from fastapi import Depends
from openai import AsyncOpenAI
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.composition.container import Container
from app.infrastructure.helpers.ai.open_ai_helper import ai_helper
from app.infrastructure.helpers.db import db_helper
from app.infrastructure.helpers.redis import redis_helper


async def get_container(
    session: AsyncSession = Depends(db_helper.session_getter),
    redis: Redis = Depends(redis_helper.get_client),
    ai_client: AsyncOpenAI = Depends(ai_helper.get_client),
) -> Container:
    return Container(session=session, redis=redis, ai_client=ai_client)
