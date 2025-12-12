class LikeNotFound(Exception):
    message = "You dont have any likes"

    def __init__(self) -> None:
        super().__init__(self.message)