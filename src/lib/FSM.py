import dataclasses

from lib.calculation import Calculation
from lib.singleton import Singleton
from lib.util import Util
from models.Vessel import Vessel


class Detector(metaclass=Singleton):
    def __init__(self, closest_vessels: list[Vessel], selected_vessel: Vessel):
        self.calculated_as_in_range: list[Vessel] = []
        self.calculated_as_not_in_range: list[Vessel] = []
        self.possible_dark_activities: list[Vessel] = []
        self.possible_out_of_range: list[Vessel] = []
        self.selected_vessel = selected_vessel
        self.estimate_positions(closest_vessels)

    def next_state(self, new_closest_vessels: list[Vessel]) -> tuple[list[Vessel], list[Vessel], tuple[int, int, int, int]]:
        false_positive_count = 0
        true_positive_count = 0
        false_negative_count = 0
        true_negative_count = 0
        self.calculate_possibilities(new_closest_vessels, self.calculated_as_in_range, self.possible_dark_activities)
        self.calculate_possibilities(new_closest_vessels, self.calculated_as_not_in_range, self.possible_out_of_range)
        self.estimate_positions(new_closest_vessels)
        for x in self.possible_dark_activities:
            if x.dark_activity is False:
                false_positive_count += 1
            else:
                true_positive_count += 1
        for x in self.possible_out_of_range:
            if x.dark_activity is True:
                false_negative_count += 1
            else:
                true_negative_count += 1

        return self.possible_dark_activities, self.possible_out_of_range, (true_positive_count, true_negative_count, false_positive_count, false_negative_count)

    @staticmethod
    def calculate_possibilities(new_closest_vessels: list[Vessel], calculated_array: list[Vessel], result_array: list[Vessel]):
        for calculated in calculated_array:
            is_found = False
            for new_closest_vessel in new_closest_vessels:
                if new_closest_vessel.mmsi == calculated.mmsi:
                    is_found = True
                    break

            if not is_found:
                for past_out_of_range in result_array:
                    if past_out_of_range.mmsi == calculated.mmsi:
                        is_found = True
                        break
                if not is_found and not calculated.is_removed:
                    result_array.append(dataclasses.replace(calculated))

    def estimate_positions(self, new_closest_vessels: list[Vessel]):
        self.calculated_as_in_range = []
        self.calculated_as_not_in_range = []
        new_estimated_position_for_selected_vessel = Calculation.calculate_destination(
            self.selected_vessel.distance_per_tick, self.selected_vessel.bearing, self.selected_vessel.position)
        for vessel in new_closest_vessels:
            new_estimated_position = Calculation.calculate_destination(vessel.distance_per_tick, vessel.bearing,
                                                                       vessel.position)
            if Util.check_range(selected_vessel_position=new_estimated_position_for_selected_vessel,
                                other_vessel_position=new_estimated_position, other_vessel_ais_range=vessel.ais_range):
                self.calculated_as_in_range.append(vessel)
            else:
                self.calculated_as_not_in_range.append(vessel)
