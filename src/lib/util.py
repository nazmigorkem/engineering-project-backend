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

        return RangeCheckResponse(normal_captured_vessels, [], [], dark_activity_vessels)

    @staticmethod
    def check_range(selected_vessel_position: LatLongExpression, other_vessel_position: LatLongExpression, other_vessel_ais_range: float | int) -> bool:
        return Calculation.calculate_distance(selected_vessel_position, other_vessel_position) < other_vessel_ais_range

    @staticmethod
    def deep_copy(array):
        new_array = []
        for x in array:
            new_array.append(dataclasses.replace(x))
        return new_array