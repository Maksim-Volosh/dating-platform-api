class PhotosNotFound(Exception):
    message = "No photos found for the given user."

    def __init__(self) -> None:
        super().__init__(self.message)


class WrongFileExtension(Exception):
    message = "You can upload only .jpg, .jpeg, .png, or .webp files."

    def __init__(self) -> None:
        super().__init__(self.message)


class TooManyPhotos(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
