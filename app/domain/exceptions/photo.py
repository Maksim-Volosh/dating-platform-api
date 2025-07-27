class PhotosNotFound(Exception):
    pass

class WrongFileExtension(Exception):
    pass

class TooManyPhotos(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
