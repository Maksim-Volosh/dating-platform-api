from app.infrastructure.api_client import api
from app.services.user.service import UserService
from app.services.photos.service import PhotoService

class Container:
    def __init__(self):
        self.api = api
        
        # Setup Services
        self.user_service = UserService(self.api)
        self.photo_service = PhotoService(self.api)

container = Container()
