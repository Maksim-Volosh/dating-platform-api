from app.infrastructure.api_client import api
from app.services import (
    DeckService,
    InboxService,
    PhotoService,
    SwipeService,
    UserService,
)


class Container:
    def __init__(self):
        self.api = api

        # Setup Services
        self.user_service = UserService(self.api)
        self.photo_service = PhotoService(self.api)
        self.inbox_service = InboxService(self.api)
        self.swipe_service = SwipeService(self.api)
        self.deck_service = DeckService(self.api)


container = Container()
