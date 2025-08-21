__all__ = (
    "IUserRepository",
    "IPhotoRepository",
    "IPhotoStorage",
    "IDeckCache",
    "ISwipeRepository",
    "ICandidateRepository",
    
)
from .deck_cache import IDeckCache
from .photo import IPhotoRepository
from .photo_storage import IPhotoStorage
from .user import IUserRepository
from .swipe import ISwipeRepository
from .candidate import ICandidateRepository
