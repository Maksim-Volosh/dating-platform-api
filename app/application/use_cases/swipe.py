from app.domain.entities import (
    FullSwipeEntity,
    InboxSwipe,
    NormalizedSwipeEntity,
    SwipeEntity,
)
from app.domain.interfaces import ISwipeRepository
from app.application.services import InboxOnSwipeService


class SwipeUserUseCase:
    def __init__(
        self, swipe_repo: ISwipeRepository, inbox_service: InboxOnSwipeService
    ) -> None:
        self.swipe_repo = swipe_repo
        self.inbox_service = inbox_service

    async def _normalize_swipe(self, swipe: SwipeEntity) -> NormalizedSwipeEntity:
        if swipe.liker_id > swipe.liked_id:
            return NormalizedSwipeEntity(
                user1_id=swipe.liked_id,
                user2_id=swipe.liker_id,
                decision=swipe.decision,
                liker_is_user1=False,
            )
        return NormalizedSwipeEntity(
            user1_id=swipe.liker_id,
            user2_id=swipe.liked_id,
            decision=swipe.decision,
            liker_is_user1=True,
        )

    async def execute(self, swipe: SwipeEntity) -> FullSwipeEntity:
        normalized_swipe = await self._normalize_swipe(swipe)
        exist_swipe = await self.swipe_repo.get_by_ids(
            normalized_swipe.user1_id, normalized_swipe.user2_id
        )
        if exist_swipe is None:
            result = await self.swipe_repo.create(normalized_swipe)
        else:
            result = await self.swipe_repo.update(exist_swipe, normalized_swipe)

        to_user_id_decision = (
            result.user2_decision
            if result.user2_id == swipe.liked_id
            else result.user1_decision
        )

        if swipe.decision:
            await self.inbox_service.create_inbox_item(
                InboxSwipe(
                    from_user_id=swipe.liker_id,
                    from_user_id_decision=swipe.decision,
                    to_user_id=swipe.liked_id,
                    to_user_id_decision=to_user_id_decision,
                )
            )
        return result
