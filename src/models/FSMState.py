from enum import Enum
from models.Vessel import Vessel
from dataclasses import dataclass


class States(Enum):
    CALCULATED_AS_IN_RANGE = 1
    CALCULATED_AS_NOT_IN_RANGE = 2
    POSSIBLE_DARK_ACTIVITY = 3


@dataclass
class FSMState:
    state: States
    vessel: Vessel
