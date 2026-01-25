class HTTPError(Exception):
    def __init__(self, status: int, body: str | None = None):
        self.status = status
        self.body = body
        super().__init__(f"HTTP {status}: {body}")
