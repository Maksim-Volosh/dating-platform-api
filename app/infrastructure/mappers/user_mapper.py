from app.domain.entities import Gender, PreferGender, UserEntity
from app.infrastructure.models import User as UserModel


class UserMapper:
    @staticmethod
    def to_entity(model: UserModel) -> UserEntity:
        return UserEntity(
            telegram_id=model.telegram_id,
            name=model.name,
            age=model.age,
            longitude=model.longitude,
            latitude=model.latitude,
            gender=Gender(model.gender),
            prefer_gender=PreferGender(model.prefer_gender),
            description=model.description,
        )

    @staticmethod
    def to_model(entity: UserEntity) -> UserModel:
        return UserModel(
            telegram_id=entity.telegram_id,
            name=entity.name,
            age=entity.age,
            longitude=entity.longitude,
            latitude=entity.latitude,
            gender=entity.gender,
            prefer_gender=entity.prefer_gender,
            description=entity.description,
        )