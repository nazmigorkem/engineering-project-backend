from dataclasses import dataclass


@dataclass
class LatLongExpression:
    latitude_in_degrees: float
    latitude_in_radians: float
    longitude_in_degrees: float
    longitude_in_radians: float
