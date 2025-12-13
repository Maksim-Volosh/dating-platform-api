from app.domain.entities import (FullSwipeEntity, MatchEntity,
                                 NormalizedMatchEntity, NormalizedSwipeEntity,
                                 SwipeEntity)
from app.domain.interfaces import ISwipeRepository


class SwipeUserUseCase:
    def __init__(self, swipe_repo: ISwipeRepository) -> None:
        self.swipe_repo = swipe_repo
        
    async def _normalize_swipe(self, swipe: SwipeEntity) -> NormalizedSwipeEntity:
        if swipe.liker_id > swipe.liked_id:
            return NormalizedSwipeEntity(
                user1_id=swipe.liked_id,
                user2_id=swipe.liker_id,
                decision=swipe.decision,
                liker_is_user1=False
            )
        return NormalizedSwipeEntity(
            user1_id=swipe.liker_id,
            user2_id=swipe.liked_id,
            decision=swipe.decision,
            liker_is_user1=True
        )
        
    async def execute(self, swipe: SwipeEntity) -> FullSwipeEntity:
        normalized_swipe = await self._normalize_swipe(swipe)
        exist_swipe = await self.swipe_repo.get_by_ids(normalized_swipe.user1_id, normalized_swipe.user2_id)
        if exist_swipe is None:
            result = await self.swipe_repo.create(normalized_swipe)
            
            return result
        
        result = await self.swipe_repo.update(normalized_swipe)
        return result if result is not None else FullSwipeEntity(
            user1_id=0,
            user1_decision=None,
            user2_id=0,
            user2_decision=None
        )
        
class SwipeMatchUserCase:
    def __init__(self, swipe_repo: ISwipeRepository) -> None:
        self.swipe_repo = swipe_repo
        
    async def _normalize_swipe(self, swipe: MatchEntity) -> NormalizedMatchEntity:
        if swipe.user2_id > swipe.user1_id:
            return NormalizedMatchEntity(
                user1_id=swipe.user1_id,
                user2_id=swipe.user2_id
            )
        return NormalizedMatchEntity(
            user1_id=swipe.user2_id,
            user2_id=swipe.user1_id
        )
        
    async def execute(self, swipe: MatchEntity) -> bool:
        normalized_match_entity: NormalizedMatchEntity = await self._normalize_swipe(swipe)
        
        result = await self.swipe_repo.is_match(normalized_match_entity)
        return result