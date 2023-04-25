from models.Vessel import Vessel
from dataclasses import dataclass
from models.LatLong import LatLongExpression


@dataclass
class Route:
    route_id: int
    from_: str
    to: str
    density: list[int]
    noise: list[int]
    coordinates: list[LatLongExpression]
    vessels: list[Vessel]
