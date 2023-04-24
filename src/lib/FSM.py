from typings.vessel import VesselType
from lib.util import Util
from enum import Enum


class States(Enum):
    NOT_IN_RANGE = 1,
    IN_RANGE = 2,
    CALCULATED_AS_IN_RANGE = 3
    CALCULATED_AS_NOT_IN_RANGE = 4
    POSSIBLE_DARK_ACTIVITY = 5


class Detector:

    def __init__(self, vessels: list[VesselType], selected_vessel: VesselType):
        self.vessel_states = []
        for vessel in vessels:
            self.vessel_states.append({
                "current_state": States.NOT_IN_RANGE,
                "vessel": vessel
            })
        self.selected_vessel = selected_vessel

    def main_loop(self):
        for state in self.vessel_states:
            match state["current_state"]:
                case States.NOT_IN_RANGE:
                    self.check_in_range(state)

    def check_in_range(self, state: dict[str, States | VesselType]):
        if Util.check_range(self.selected_vessel, state["vessel"]):
            if state["current_state"] == States.NOT_IN_RANGE:
                state["current_state"] = States.IN_RANGE
