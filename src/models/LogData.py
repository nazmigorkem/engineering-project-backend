from dataclasses import dataclass, asdict

from models.RangeCheckResponse import RangeCheckResponse
from models.Vessel import Vessel


@dataclass
class LogData:
    tick_number: int
    generated_vessels: list[Vessel]
    range_check: RangeCheckResponse
    total_dark_activity_vessels: list[Vessel]

    @property
    def __dict__(self):
        return asdict(self)
