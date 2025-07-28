from app.domain.entities import UserEntity
from app.infrastructure.models import User as UserModel


class UserMapper:
    @staticmethod
    def to_entity(model: UserModel) -> UserEntity:
        return UserEntity(
            telegram_id=model.telegram_id,
            name=model.name,
            age=model.age,
            city=model.city,
            gender=model.gender,
            prefer_gender=model.prefer_gender,
            description=model.description,
        )

    @staticmethod
    def to_model(entity: UserEntity) -> UserModel:
        return UserModel(
            telegram_id=entity.telegram_id,
            name=entity.name,
            age=entity.age,
            city=entity.city,
            gender=entity.gender,
            prefer_gender=entity.prefer_gender,
            description=entity.description,
        )
