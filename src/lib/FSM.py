from lib.calculation import Calculation
from models.Vessel import Vessel
from lib.singleton import Singleton
from lib.util import Util


class Detector(metaclass=Singleton):
    def __init__(self, closest_vessels: list[Vessel], selected_vessel: Vessel):
        self.calculated_as_in_range: list[Vessel] = []
        self.calculated_as_not_in_range: list[Vessel] = []
        self.possible_dark_activities: list[Vessel] = []
        self.selected_vessel = selected_vessel
        self.estimate_positions(closest_vessels)

    def next_state(self, new_closest_vessels: list[Vessel]):
        for calculated_as_in_range in self.calculated_as_in_range:
            is_found = False
            for new_closest_vessel in new_closest_vessels:
                if new_closest_vessel.mmsi == calculated_as_in_range.mmsi:
                    is_found = True
                    break
            if not is_found:
                self.possible_dark_activities.append(calculated_as_in_range)
        self.estimate_positions(new_closest_vessels)
        print(list(map(lambda x: x.mmsi, self.possible_dark_activities)))

    def estimate_positions(self, new_closest_vessels: list[Vessel]):
        self.calculated_as_in_range = []
        self.calculated_as_not_in_range = []
        new_estimated_position_for_selected_vessel = Calculation.calculate_destination(self.selected_vessel.distance_per_tick, self.selected_vessel.bearing, self.selected_vessel.position)
        for vessel in new_closest_vessels:
            new_estimated_position = Calculation.calculate_destination(vessel.distance_per_tick, vessel.bearing, vessel.position)
            if Util.check_range(selected_vessel_position=new_estimated_position_for_selected_vessel, other_vessel_position=new_estimated_position, other_vessel_ais_range=vessel.ais_range):
                self.calculated_as_in_range.append(vessel)
            else:
                # not used at the moment, added for future features
                self.calculated_as_not_in_range.append(vessel)
