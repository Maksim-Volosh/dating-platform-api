class NoCandidatesFound(Exception):
    message = "Unfortunately, at this moment, we couldn't find any candidates that meet your criteria. Please check back later or adjust your preferences for better results."

    def __init__(self) -> None:
        super().__init__(self.message)