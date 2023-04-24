from models import Vessel
from dataclasses import dataclass


@dataclass
class Route:
    route_id: int
    _from: str
    to: str
    density: list[int]
    noise: list[int]
    coordinates: list[tuple[int, int]]
    vessels: list[Vessel]
