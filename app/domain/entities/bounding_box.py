from dataclasses import dataclass


@dataclass
class BBoxEntity:
    min_latitude: float
    max_latitude: float
    min_longitude: float
    max_longitude: float