from app.infrastructure.api_client import api
from app.services.user.service import UserService

class Container:
    def __init__(self):
        self.api = api
        self.user_service = UserService(self.api)

container = Container()
