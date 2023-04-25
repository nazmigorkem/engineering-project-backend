from enum import Enum
from models.Vessel import Vessel
from lib.singleton import Singleton


class States(Enum):
    FIRST_CAPTURE = 1
    CALCULATED_AS_IN_RANGE = 2
    CALCULATED_AS_NOT_IN_RANGE = 3
    POSSIBLE_DARK_ACTIVITY = 4


class Detector(metaclass=Singleton):
    vessel_states = []
    selected_vessel = None

    def __init__(self,  vessels: list[Vessel], selected_vessel: Vessel):
        self.vessel_states = []
        self.selected_vessel = selected_vessel
