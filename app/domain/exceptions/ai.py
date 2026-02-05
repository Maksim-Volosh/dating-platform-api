class AIUnavailableError(Exception):
    message = "Unfortunately, the AI service is unavailable at the moment. Please try again later."

    def __init__(self) -> None:
        super().__init__(self.message)
