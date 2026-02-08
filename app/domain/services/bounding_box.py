from math import cos, radians

from app.domain.entities import BBoxEntity


def bounding_box(lat: float, lon: float, radius_km: float) -> BBoxEntity:
    """
    Calculate bounding box coordinates for a given latitude, longitude and radius in kilometers.

    Args:
        lat (float): Latitude in degrees.
        lon (float): Longitude in degrees.
        radius_km (float): Radius in kilometers.

    Returns:
        tuple[float, float, float, float]: A tuple containing the minimum and maximum latitude and longitude.
    """

    lat_delta = radius_km / 111.0
    lon_delta = radius_km / (111.0 * cos(radians(lat)))

    return BBoxEntity(
        min_latitude=lat - lat_delta,
        max_latitude=lat + lat_delta,
        min_longitude=lon - lon_delta,
        max_longitude=lon + lon_delta,
    )
