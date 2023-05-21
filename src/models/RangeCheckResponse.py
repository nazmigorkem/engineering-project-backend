from dataclasses import dataclass

from models.Vessel import Vessel


@dataclass
class RangeCheckResponse:
    closest_vessels: list[Vessel]
    detected_dark_activity_vessels: list[Vessel]
    all_dark_activity_vessels: list[Vessel]
