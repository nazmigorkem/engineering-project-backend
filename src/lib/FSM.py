from typings.vessel import VesselType
from lib.util import Util
from enum import Enum
from lib.calculation import Calculation
from lib.singleton import Singleton


class States(Enum):
    FIRST_CAPTURE = 1
    CALCULATED_AS_IN_RANGE = 2
    CALCULATED_AS_NOT_IN_RANGE = 3
    POSSIBLE_DARK_ACTIVITY = 4


class Detector(metaclass=Singleton):
    vessel_states = []
    selected_vessel = None

    def __init__(self,  vessels: list[VesselType], selected_vessel: VesselType):
        self.vessel_states = []
        for vessel in vessels:
            self.vessel_states.append({
                "current_state": States.FIRST_CAPTURE,
                "vessel": vessel
            })
        self.selected_vessel = selected_vessel

    def main_loop(self):
        for state in self.vessel_states:
            match state["current_state"]:
                case States.FIRST_CAPTURE:
                    self.check_in_range(state)

        print(self.vessel_states)

    def check_in_range(self, state: dict[str, States | VesselType]):
        vessel = state["vessel"]

        calculated_destination_for_other_vessel = Calculation.calculate_destination(vessel.distance_per_tick,
                                                                                    vessel.bearing, vessel.lat,
                                                                                    vessel.lon)
        calculated_destination_for_selected_vessel = Calculation.calculate_destination(
            self.selected_vessel.distance_per_tick, self.selected_vessel.bearing, self.selected_vessel.lat,
            self.selected_vessel.lon)
        updated_other_vessel = {
            "aisRange": vessel.aisRange,
            "lat": calculated_destination_for_other_vessel[0],
            "lon": calculated_destination_for_other_vessel[1],
        }
        updated_selected_vessel = {
            "lat": calculated_destination_for_selected_vessel[0],
            "lon": calculated_destination_for_selected_vessel[1],
        }
        if Util.check_range(updated_selected_vessel, updated_other_vessel):
            state["current_state"] = States.CALCULATED_AS_IN_RANGE
        else:
            state["current_state"] = States.CALCULATED_AS_NOT_IN_RANGE
