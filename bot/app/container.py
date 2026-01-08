from app.infrastructure.api_client import api
from app.services import InboxService, PhotoService, UserService, SwipeService


class Container:
    def __init__(self):
        self.api = api
        
        # Setup Services
        self.user_service = UserService(self.api)
        self.photo_service = PhotoService(self.api)
        self.inbox_service = InboxService(self.api)
        self.swipe_service = SwipeService(self.api)

container = Container()
