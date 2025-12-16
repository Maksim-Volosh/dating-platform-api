class InboxItemNotFound(Exception):
    message = "You dont have any inbox items"

    def __init__(self) -> None:
        super().__init__(self.message)