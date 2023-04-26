from dataclasses import dataclass
from models.Vessel import Vessel


@dataclass
class RangeCheckResponse:
    closest_vessels: list[Vessel]
    closest_dark_activity_vessels: list[Vessel]
