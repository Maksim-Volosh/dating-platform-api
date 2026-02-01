from app.core.config import settings
from app.domain.entities import UserDistanceEntity, UserEntity
from app.domain.services.haversine import haversine
from app.infrastructure.mappers.user_mapper import UserMapper


class GeoCandidateFilterService:
    def filter(
        self,
        user: UserEntity,
        candidates: list[UserEntity],
    ) -> list[UserDistanceEntity] | None:
        result: list[UserDistanceEntity] = []
        
        for step in settings.deck.radius_steps_km:
            for candidate in candidates:
                distance = haversine(user.latitude, user.longitude, candidate.latitude, candidate.longitude)
                if distance <= step:
                    result.append(UserMapper.to_user_distance_entity(candidate, distance))
            if result:
                return result
        return None
        
        
