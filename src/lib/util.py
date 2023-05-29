import dataclasses
from builtins import int

from lib.calculation import Calculation
from models.LatLong import LatLongExpression
from models.RangeCheckResponse import RangeCheckResponse
from models.Vessel import Vessel


class Util:
    
    @staticmethod
    def find_in_range(arr: list[Vessel], selected_vessel: Vessel) -> RangeCheckResponse:
        normal_captured_vessels = []
        dark_activity_vessels = []
        for x in arr:
            if x.mmsi != selected_vessel.mmsi and Util.check_range(selected_vessel.position, x.position, x.ais_range):
                if not x.dark_activity:
                    normal_captured_vessels.append(x)
                else:
                    dark_activity_vessels.append(x)

        return RangeCheckResponse(normal_captured_vessels, [], [], [], [], dark_activity_vessels)

    @staticmethod
    def check_range(selected_vessel_position: LatLongExpression, other_vessel_position: LatLongExpression, other_vessel_ais_range: float | int) -> bool:
        return Calculation.calculate_distance(selected_vessel_position, other_vessel_position) < other_vessel_ais_range

    @staticmethod
    def deep_copy(array):
        new_array = []
        for x in array:
            new_array.append(dataclasses.replace(x))
        return new_array

    @staticmethod
    def calculate_confusion_matrix(possible_dark_activities, possible_out_of_range):
        false_negative_count = 0
        true_negative_count = 0
        false_positive_count = 0
        true_positive_count = 0
        for x in possible_dark_activities:
            if x.dark_activity is False:
                false_negative_count += 1
            else:
                true_negative_count += 1

        for x in possible_out_of_range:
            if x.dark_activity is True:
                false_positive_count += 1
            else:
                true_positive_count += 1

        return true_positive_count, false_positive_count, false_negative_count, true_negative_count

    @staticmethod
    def append_if_does_not_exist(results, target_array):
        for x in results:
            is_found = False
            for y in target_array:
                if x.mmsi == y.mmsi:
                    is_found = True
                    break
            if not is_found:
                target_array.append(dataclasses.replace(x))
                