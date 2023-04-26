from dataclasses import dataclass

from models.RangeCheckResponse import RangeCheckResponse
from models.Route import Route


@dataclass
class GenerateResponse:
    generated_vessels: list[Route]
    range_check: RangeCheckResponse
