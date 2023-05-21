from dataclasses import dataclass

from models.LatLong import LatLongExpression
from models.Vessel import Vessel


@dataclass
class Route:
    route_id: int
    from_: str
    to: str
    density: list[int]
    noise: list[int]
    coordinates: list[LatLongExpression]
    vessels: list[Vessel]
