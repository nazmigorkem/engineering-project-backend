import csv
import dataclasses
import random

from lib.calculation import Calculation
from lib.simulation import Simulation
from models.GenerateResponse import GenerateResponse
from models.LogData import LogData
from models.Vessel import Vessel


class NonVisualSimulation:

    def __init__(self):
        self.field_names = ["distance_from_selected_vessel", "selected_vessel_course", "selected_vessel_heading", "selected_vessel_distance_per_tick", "selected_vessel_distance_to_turn_point", "course", "heading", "distance_per_tick", "distance_to_turn_point", "ais_range", "dark_activity"]
        self.data = []
        self.logs_as_dict: list[dict[str, any]] = []
        self.total_dark_activities = []
        self.simulation: Simulation | None = None
        self.total_confusion_matrix_fsm = (0, 0, 0, 0)
        self.total_confusion_matrix_ml = (0, 0, 0, 0)
        for i in range(10):
            print(f"\033[35mIteration #{i + 1}\033[0m")
            self.setup()
            self.iteration(1000)
            print(f"Done.")
            print(f"\033[31;1m{len(self.simulation.total_dark_activity_for_whole_simulation_fsm)}\033[0;22m total dark activities found by FSM")
            print(f"FSM confusion matrix: {self.simulation.confusion_matrix_fsm}")
            print(f"\033[31;1m{len(self.simulation.total_dark_activity_for_whole_simulation_ml)}\033[0;22m total dark activities found by ML")
            print(f"ML Confusion matrix: {self.simulation.confusion_matrix_ml}")
            self.total_confusion_matrix_fsm = tuple(map(sum, zip(self.total_confusion_matrix_fsm, self.simulation.confusion_matrix_fsm)))
            self.total_confusion_matrix_ml = tuple(map(sum, zip(self.total_confusion_matrix_ml, self.simulation.confusion_matrix_ml)))
        print(f"FSM Confusion matrix {self.total_confusion_matrix_fsm} Accuracy: {(self.total_confusion_matrix_fsm[0] + self.total_confusion_matrix_fsm[3]) / (self.total_confusion_matrix_fsm[0] + self.total_confusion_matrix_fsm[1] + self.total_confusion_matrix_fsm[2] + self.total_confusion_matrix_fsm[3])}")
        print(f"ML Confusion matrix {self.total_confusion_matrix_ml}  Accuracy: {(self.total_confusion_matrix_ml[0] + self.total_confusion_matrix_ml[3]) / (self.total_confusion_matrix_ml[0] + self.total_confusion_matrix_ml[1] + self.total_confusion_matrix_ml[2] + self.total_confusion_matrix_ml[3])}")
        self.export_results()

    def setup(self):
        Simulation.clear()
        self.simulation = Simulation()
        self.simulation.start_simulation()

    def iteration(self, tick_count: int):
        previous_tick_closest_vessels: list[Vessel] = []
        for i in range(1, tick_count + 1):

            current_tick: GenerateResponse = self.simulation.next_tick()
            print(f"Tick {i}")
            if i % 10 == 0 or self.simulation.selected_vessel is None:
                self.simulation.fsm_detector.clear()
                self.simulation.ml_detector.clear()
                self.simulation.selected_vessel = random.choice(self.simulation.vessels_ordered_by_mmsi)

            dark_activity_vessel: Vessel = random.choice(self.simulation.vessels_ordered_by_mmsi)
            if dark_activity_vessel != self.simulation.selected_vessel:
                dark_activity_vessel.dark_activity = True

            if i != 0:
                self.iterate_results(current_tick.range_check.current_tick_detected_dark_activity_vessels_by_fsm)
                self.iterate_results(current_tick.range_check.detected_out_of_range_vessels_by_fsm)
                # previous_tick_closest_vessels = Util.deep_copy(current_tick.range_check.closest_vessels)
                self.logs_as_dict.append(
                    LogData(i, dataclasses.replace(self.simulation.selected_vessel), current_tick.range_check).__dict__)
            print("\033[1A\033[0K", end="")

    def iterate_results(self, results: list[Vessel]):
        for x in results:
            self.data.append({"distance_from_selected_vessel": Calculation.calculate_distance(self.simulation.selected_vessel.position, x.position),
                              "selected_vessel_course": self.simulation.selected_vessel.course,
                              "selected_vessel_heading": self.simulation.selected_vessel.heading,
                              "selected_vessel_distance_per_tick": self.simulation.selected_vessel.distance_per_tick,
                              "selected_vessel_distance_to_turn_point": self.simulation.selected_vessel.last_distance_to_current_mid_point_end,
                              "course": x.course,
                              "heading": x.heading,
                              "distance_per_tick": x.distance_per_tick,
                              "distance_to_turn_point": x.last_distance_to_current_mid_point_end,
                              "ais_range": x.ais_range,
                              "dark_activity": x.dark_activity})

    def export_results(self):
        with open('data.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.field_names)
            writer.writeheader()
            writer.writerows(self.data)

        # self.logs_as_dict.append(
        #     {"total_dark_activities": list(
        #         map(lambda y: y.__dict__, self.simulation.total_dark_activity_for_whole_simulation))})

        # with open("output.json", "w") as outfile:
        #     outfile.write(json.dumps(self.logs_as_dict, indent=4))

    def compare_with_previous_tick(self, current_tick_array, previous_tick_closest_vessels, target_array):
        for x in current_tick_array:
            for y in previous_tick_closest_vessels:
                if x.mmsi == y.mmsi:
                    target_array.append(dataclasses.replace(y))
                    break


NonVisualSimulation()
