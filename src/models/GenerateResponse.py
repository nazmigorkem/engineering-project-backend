from dataclasses import dataclass, asdict, field
from json import dumps

from models.RangeCheckResponse import RangeCheckResponse
from models.Route import Route
from models.Vessel import Vessel


@dataclass
class GenerateResponse:
    generated_vessels: list[Route]
    range_check: RangeCheckResponse
    total_dark_activity_vessels: list[Vessel]


