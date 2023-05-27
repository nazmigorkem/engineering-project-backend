from dataclasses import dataclass

from models.RangeCheckResponse import RangeCheckResponse
from models.Route import Route
from models.Vessel import Vessel


@dataclass
class GenerateResponse:
    generated_vessels: list[Route]
    range_check: RangeCheckResponse
    total_dark_activity_vessels_fsm: list[Vessel]
    total_dark_activity_vessels_ml: list[Vessel]
    confusion_matrix_fsm: tuple[int, int, int, int]
    confusion_matrix_ml: tuple[int, int, int, int]
