from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.schemas.like import LikeCreateResponse, LikeNextResponse, LikeRequest
from app.core.containers.like import get_like_use_case
from app.domain.exceptions import LikeNotFound
from app.domain.use_cases import LikeUseCase

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/add_like/{liked_id}", status_code=201)
async def create_like(
    liked_id: int,
    body: LikeRequest,
    use_case: LikeUseCase = Depends(get_like_use_case)
) -> LikeCreateResponse:
    count = await use_case.add_like(liked_id, body.liker_id)
    
    return LikeCreateResponse(count=count)

@router.get("/pending/{liked_id}", status_code=201)
async def get_next_like(
    liked_id: int,
    use_case: LikeUseCase = Depends(get_like_use_case)
) -> LikeNextResponse:
    try:
        liker_id = await use_case.get_next_like(liked_id)
    except LikeNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    
    return LikeNextResponse(liker_id=liker_id)

@router.get("/pending/count/{liked_id}", status_code=200)
async def get_like_count(
    liked_id: int,
    use_case: LikeUseCase = Depends(get_like_use_case)
) -> LikeCreateResponse:
    count = await use_case.get_count(liked_id)
    
    return LikeCreateResponse(count=count)

@router.delete("/pending/{liked_id}", status_code=204)
async def remove_like(
    liked_id: int,
    use_case: LikeUseCase = Depends(get_like_use_case)
):
    await use_case.remove_like(liked_id)
    
    return