from app.core.config import settings
from app.domain.entities import UserDistanceEntity, UserEntity
from app.domain.services.haversine import haversine


class GeoCandidateFilterService:
    async def filter(
        self,
        user: UserEntity,
        candidates: list[UserEntity],
    ) -> list[UserDistanceEntity]:
        result: list[UserDistanceEntity] = []
        
        for step in settings.deck.radius_steps_km:
            for candidate in candidates:
                distance = haversine(user.latitude, user.longitude, candidate.latitude, candidate.longitude)
                if distance <= step:
                    result.append(
                        UserDistanceEntity(
                            telegram_id=candidate.telegram_id,
                            name=candidate.name,
                            age=candidate.age,
                            distance=distance,
                            gender=candidate.gender,
                            prefer_gender=candidate.prefer_gender,
                            description=candidate.description,
                        )
                    )
            if result:
                return result
        return []
        
        
