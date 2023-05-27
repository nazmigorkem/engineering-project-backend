import dataclasses

from joblib import load

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
        self.previous_closest_vessels = Util.deep_copy(closest_vessels)
        self.selected_vessel = selected_vessel
        self.selected_vessel_previous_tick = dataclasses.replace(selected_vessel)
        self.clf = load('trained_model.joblib')

    def next_state(self, new_closest_vessels: list[Vessel]) -> tuple[list[Vessel], list[Vessel], tuple[int, int, int, int]]:
        false_positive_count = 0
        true_positive_count = 0
        false_negative_count = 0
        true_negative_count = 0
        suspects = []
        for x in self.previous_closest_vessels:
            is_found = False
            for y in new_closest_vessels:
                if x.mmsi == y.mmsi:
                    is_found = True
                    break
            if not is_found and not x.is_removed:
                suspects.append(x)

        for x in suspects:
            if self.clf.predict([[
                Calculation.calculate_distance(self.selected_vessel_previous_tick.position, x.position),
                self.selected_vessel.course,
                self.selected_vessel_previous_tick.heading,
                self.selected_vessel_previous_tick.distance_per_tick,
                self.selected_vessel_previous_tick.last_distance_to_current_mid_point_end,
                x.course,
                x.heading,
                x.distance_per_tick,
                x.last_distance_to_current_mid_point_end,
                x.ais_range,
            ]])[0] == 1:
                self.possible_dark_activities.append(x)
            else:
                self.possible_out_of_range.append(x)

        self.selected_vessel_previous_tick = dataclasses.replace(self.selected_vessel)
        self.previous_closest_vessels = new_closest_vessels
        for x in self.possible_dark_activities:
            if not x.dark_activity:
                false_positive_count += 1
            else:
                true_positive_count += 1
        for x in self.possible_out_of_range:
            if x.dark_activity:
                false_negative_count += 1
            else:
                true_negative_count += 1

        return self.possible_dark_activities, self.possible_out_of_range, (true_positive_count, true_negative_count, false_positive_count, false_negative_count)

