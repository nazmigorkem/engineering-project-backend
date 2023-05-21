import dataclasses
import json
from builtins import int

from lib.calculation import Calculation
from models.LatLong import LatLongExpression
from models.RangeCheckResponse import RangeCheckResponse
from models.Vessel import Vessel


class Util:
    @staticmethod
    def dump(path: str, item):
        json_dump = json.dumps(item, indent=2)
        with open(path, "w") as out_f:
            out_f.write(json_dump)

    @staticmethod
    def serialize_dataclass_array(array):
        return list(map(lambda x: dataclasses.asdict(x), array))

    @staticmethod
    def insert_sorted(arr, x, sort_by=None):
        left = 0
        right = len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if (sort_by is not None and arr[mid][sort_by] == x[sort_by]) or (
                    sort_by is None and arr[mid][sort_by] == x[sort_by]):
                while mid < len(arr) and (sort_by is not None and arr[mid][sort_by] == x[sort_by]) or (
                        sort_by is None and arr[mid][sort_by] == x[sort_by]):
                    mid += 1
                arr.insert(mid, x)
                return
            elif (sort_by is not None and arr[mid][sort_by] < x[sort_by]) or (
                    sort_by is None and arr[mid][sort_by] < x[sort_by]):
                left = mid + 1
            else:
                right = mid - 1
        arr.insert(left, x)

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

        return RangeCheckResponse(normal_captured_vessels, dark_activity_vessels)

    @staticmethod
    def check_range(selected_vessel_position: LatLongExpression, other_vessel_position: LatLongExpression,
                    other_vessel_ais_range: float | int) -> bool:
        return Calculation.calculate_distance(selected_vessel_position, other_vessel_position) < other_vessel_ais_range
