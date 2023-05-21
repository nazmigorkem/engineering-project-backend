from dataclasses import dataclass, asdict

from models.RangeCheckResponse import RangeCheckResponse
from models.Vessel import Vessel


@dataclass
class LogData:
    tick_number: int
    selected_vessel: Vessel
    range_check: RangeCheckResponse

    @property
    def __dict__(self):
        return asdict(self)
