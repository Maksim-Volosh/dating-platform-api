from fastapi import Depends, Header, HTTPException, status

from app.application.use_cases import UserUseCase
from app.core.config import settings
from app.core.containers.user import get_user_use_case
from app.domain.entities import UserEntity
from app.domain.exceptions import UserNotFoundById


async def verify_bot_key(x_api_key: str = Header(...)):
    if x_api_key not in settings.security.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Client API Key")
        
async def get_existing_user(
    telegram_id: int,
    use_case: UserUseCase = Depends(get_user_use_case),
) -> UserEntity:
    try:
        return await use_case.get_by_id(telegram_id)
    except UserNotFoundById as e:
        raise HTTPException(status_code=404, detail=e.message)
