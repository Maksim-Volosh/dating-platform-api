__all__ = (
    "IUserRepository",
    "IPhotoRepository"
)
from .user import IUserRepository
from .photo import IPhotoRepository
from .photo_storage import IPhotoStorage