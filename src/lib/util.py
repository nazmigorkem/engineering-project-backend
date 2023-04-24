import json
from lib.calculation import Calculation
class Util:
    @staticmethod
    def dump(path: str, item):
        json_dump = json.dumps(item, indent=2)
        with open(path, "w") as out_f:
            out_f.write(json_dump)

    @staticmethod
    def insert_sorted(arr, x, sort_by = None):
        left = 0
        right = len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if (sort_by is not None and arr[mid][sort_by] == x[sort_by]) or (sort_by is None and arr[mid][sort_by] == x[sort_by]):
                while mid < len(arr) and (sort_by is not None and arr[mid][sort_by] == x[sort_by]) or (sort_by is None and arr[mid][sort_by] == x[sort_by]):
                    mid += 1
                arr.insert(mid, x)
                return
            elif (sort_by is not None and arr[mid][sort_by] < x[sort_by]) or (sort_by is None and arr[mid][sort_by] < x[sort_by]):
                left = mid + 1
            else:
                right = mid - 1
        arr.insert(left, x)

    @staticmethod
    def find_in_range(arr, selected_vessel):
        final_arr = []

        for x in arr:
            if x["mmsi"] != selected_vessel["mmsi"] and Util.check_range(selected_vessel, x):
                final_arr.append(x)

        return final_arr

    @staticmethod
    def check_range(selected_vessel, other_vessel) -> bool:
        return Calculation.calculate_distance(selected_vessel["lat"], selected_vessel["lon"], other_vessel["lat"], other_vessel["lon"]) < other_vessel["aisRange"]