__all__ = (
    "IUserRepository",
    "IPhotoRepository",
    "IPhotoStorage",
    "IDeckCache",
    
)
from .user import IUserRepository
from .photo import IPhotoRepository
from .photo_storage import IPhotoStorage
from .deck_cache import IDeckCache