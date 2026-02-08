class RateLimitTooManyRequests(Exception):
    message = "Too many requests. Please try again later."

    def __init__(self) -> None:
        super().__init__(self.message)
