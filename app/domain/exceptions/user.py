class UserNotFoundById(Exception):
    message = "User with given telegram_id not found."

    def __init__(self) -> None:
        super().__init__(self.message)


class UsersNotFound(Exception):
    message = "No users found in the database."

    def __init__(self) -> None:
        super().__init__(self.message)


class UserAlreadyExists(Exception):
    message = "User with given telegram_id already exists in the database. Please try to create new user with different telegram_id"

    def __init__(self) -> None:
        super().__init__(self.message)
