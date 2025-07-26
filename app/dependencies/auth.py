from fastapi import Header, HTTPException, status

from app.config import settings


async def verify_bot_key(x_api_key: str = Header(...)):
    if x_api_key not in settings.security.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Client API Key")