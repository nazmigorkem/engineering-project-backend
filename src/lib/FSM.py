from enum import Enum
from models.Vessel import Vessel
from lib.singleton import Singleton
from models.FSMState import FSMState, States


class Detector(metaclass=Singleton):
    def __init__(self, closest_vessels: list[Vessel], selected_vessel: Vessel):
        self.vessel_states: list[FSMState] = []
        for vessel in closest_vessels:
            self.vessel_states.append(FSMState(States.CALCULATED_AS_IN_RANGE, vessel))
        self.selected_vessel = selected_vessel

    def next_state(self, new_closest_vessels: list[Vessel]):
        pass
