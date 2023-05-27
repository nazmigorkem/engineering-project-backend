import dataclasses
import json
import math
import random

from lib.FSM import Detector as FSMDetector
from lib.calculation import Calculation
from lib.machine_learning import Detector as MLDetector
from lib.singleton import Singleton
from lib.util import Util
from models.GenerateResponse import GenerateResponse
from models.LatLong import LatLongExpression
from models.RangeCheckResponse import RangeCheckResponse
from models.Route import Route
from models.Vessel import Vessel
from models.VesselType import VesselType, ValueField


class Simulation(metaclass=Singleton):
    def __init__(self):
        self.types: list[VesselType] = []
        self.routes: list[Route] = []
        self.confusion_matrix_fsm = (0, 0, 0, 0)
        self.confusion_matrix_ml = (0, 0, 0, 0)
        self.fsm_detector = FSMDetector
        self.ml_detector = MLDetector

        with open('./data/vessel_types.json') as f:
            types = json.load(f)["vesselTypes"]
        for x in types:
            length = x["length"]
            speed = x["speed"]
            ais_range = x["aisRange"]
            ais_broadcast_interval = x["aisBroadcastInterval"]
            self.types.append(VesselType(name=x["name"],
                                         length=ValueField(value=length["value"], unit=length["unit"]),
                                         speed=ValueField(value=speed["value"], unit=speed["unit"]),
                                         ais_range=ValueField(value=ais_range["value"], unit=ais_range["unit"]),
                                         ais_broadcast_interval=ValueField(value=ais_broadcast_interval["value"],
                                                                           unit=ais_broadcast_interval["unit"])))

        with open('./data/routes.json') as f:
            raw_route_data = json.load(f)
        for raw_route in raw_route_data:
            coordinates = raw_route["coordinates"]
            lat_long_expressions: list[LatLongExpression] = []
            for coordinate in coordinates:
                lat_long_expressions.append(LatLongExpression(latitude_in_degrees=coordinate[0],
                                                              latitude_in_radians=math.radians(coordinate[0]),
                                                              longitude_in_degrees=coordinate[1],
                                                              longitude_in_radians=math.radians(coordinate[1])))
            route = Route(route_id=raw_route["route_id"],
                          from_=raw_route["from"],
                          to=raw_route["to"],
                          coordinates=lat_long_expressions,
                          vessels=[],
                          density=raw_route["density"], noise=raw_route["noise"])
            self.routes.append(route)
        self.tick_rate = 60
        self.mmsi_starting_number = 10_000_000
        self.mmsi = self.mmsi_starting_number
        self.vessels_ordered_by_mmsi: list[Vessel] = []
        self.total_dark_activity_for_whole_simulation_fsm: list[Vessel] = []
        self.total_dark_activity_for_whole_simulation_ml: list[Vessel] = []
        self.selected_vessel: Vessel | None = None
        self.is_simulation_started = False
        print('Vessels are generated')

    def next_tick(self) -> GenerateResponse:
        broadcast_control = RangeCheckResponse([], [], [], [], [], [])
        detected_dark_activities_by_fsm = []
        detected_out_of_range_by_fsm = []
        detected_dark_activities_by_ml = []
        detected_out_of_range_by_ml = []
        confusion_matrix_fsm = (0, 0, 0, 0)
        confusion_matrix_ml = (0, 0, 0, 0)

        for route in self.routes:
            for vessel in route.vessels:
                index = vessel.current_route_index
                current_route = route.coordinates[index]
                current_destination = route.coordinates[
                    (index + 1) if not vessel.is_going_reverse_route else (index - 1)]
                distance = Calculation.calculate_distance(current_destination, vessel.position)
                slope = math.degrees(Calculation.calculate_bearing(current_route, current_destination))

                if vessel.course != slope:
                    vessel.course = slope
                elif random.random() < 0.5:
                    vessel.course = vessel.course + (vessel.course / 8 * (1 if random.random() < 0.5 else -1))

                if vessel.last_distance_to_current_mid_point_end < distance:
                    if (not vessel.is_going_reverse_route and len(route.coordinates) == index + 2) or (
                            vessel.is_going_reverse_route and index - 2 == -1):
                        route.vessels.remove(vessel)
                        self.vessels_ordered_by_mmsi[vessel.mmsi - self.mmsi_starting_number].is_removed = True

                        if self.selected_vessel is not None and self.selected_vessel.mmsi == vessel.mmsi:
                            self.selected_vessel = None
                        if random.random() < 0.5:
                            new_vessel = self.generate(route.coordinates[0], route.coordinates[1], 0, 1, route.noise[0],
                                                       (True, False))[0]
                        else:
                            new_vessel = \
                                self.generate(route.coordinates[-2], route.coordinates[-1], len(route.coordinates) - 2,
                                              1,
                                              route.noise[-1], (True, True))[0]
                        route.vessels.append(new_vessel)
                        continue

                    next_destination = route.coordinates[
                        (index + 2) if not vessel.is_going_reverse_route else (index - 2)]
                    slope = Calculation.calculate_bearing(current_destination, next_destination)
                    vessel.course = math.degrees(slope)

                    current_destination = next_destination
                    vessel.current_route_index = (index + 1) if not vessel.is_going_reverse_route else (index - 1)
                    distance = Calculation.calculate_distance(current_destination, vessel.position)
                vessel.last_distance_to_current_mid_point_end = distance
                vessel.bearing = vessel.course
                vessel.position = Calculation.calculate_destination(vessel.distance_per_tick, vessel.bearing,
                                                                    vessel.position)

                if (not vessel.is_going_reverse_route and not len(route.coordinates) == index + 2) or (
                        not vessel.is_going_reverse_route and index - 2 == -1):
                    next_destination = route.coordinates[
                        (index + 2) if not vessel.is_going_reverse_route else (index - 2)]
                    vessel.heading = math.degrees(Calculation.calculate_bearing(vessel.position, next_destination))

        if self.selected_vessel is not None:
            broadcast_control = self.find_closest_vessels_of_selected_vessel()
            detected_dark_activities_by_fsm, detected_out_of_range_by_fsm, confusion_matrix_fsm = self.fsm_detector(
                closest_vessels=broadcast_control.closest_vessels,
                selected_vessel=self.selected_vessel).next_state(broadcast_control.closest_vessels)
            detected_dark_activities_by_ml, detected_out_of_range_by_ml, confusion_matrix_ml = self.ml_detector(
                closest_vessels=broadcast_control.closest_vessels,
                selected_vessel=self.selected_vessel).next_state(broadcast_control.closest_vessels)

            for x in detected_dark_activities_by_fsm:
                is_found = False
                for y in self.total_dark_activity_for_whole_simulation_fsm:
                    if x.mmsi == y.mmsi:
                        is_found = True
                        break
                if not is_found:
                    self.total_dark_activity_for_whole_simulation_fsm.append(dataclasses.replace(x))

            for x in detected_dark_activities_by_ml:
                is_found = False
                for y in self.total_dark_activity_for_whole_simulation_ml:
                    if x.mmsi == y.mmsi:
                        is_found = True
                        break
                if not is_found:
                    self.total_dark_activity_for_whole_simulation_ml.append(dataclasses.replace(x))

        self.confusion_matrix_fsm = tuple(map(sum, zip(self.confusion_matrix_fsm, confusion_matrix_fsm)))
        self.confusion_matrix_ml = tuple(map(sum, zip(self.confusion_matrix_ml, confusion_matrix_ml)))
        return GenerateResponse(self.routes,
                                RangeCheckResponse(closest_vessels=broadcast_control.closest_vessels,
                                                   detected_dark_activity_vessels_by_fsm=detected_dark_activities_by_fsm,
                                                   detected_out_of_range_vessels_by_fsm=detected_out_of_range_by_fsm,
                                                   detected_dark_activity_vessels_by_ml=detected_dark_activities_by_ml,
                                                   detected_out_of_range_vessels_by_ml=detected_out_of_range_by_ml,
                                                   all_dark_activity_vessels=broadcast_control.all_dark_activity_vessels),
                                total_dark_activity_vessels_fsm=self.total_dark_activity_for_whole_simulation_fsm,
                                total_dark_activity_vessels_ml=self.total_dark_activity_for_whole_simulation_ml,
                                confusion_matrix_fsm=confusion_matrix_fsm,
                                confusion_matrix_ml=confusion_matrix_ml)

    def start_simulation(self) -> GenerateResponse:
        for (ith_route, route) in enumerate(self.routes):
            for (i, (from_, to)) in enumerate(zip(route.coordinates[:-1], route.coordinates[1:])):
                for y in self.generate(from_, to, i, route.density[i], route.noise[i]):
                    self.routes[ith_route].vessels.append(y)
        self.is_simulation_started = True
        return GenerateResponse(self.routes, RangeCheckResponse([], [], [], [], [], []), [], [], (0, 0, 0, 0),
                                (0, 0, 0, 0))

    def find_closest_vessels_of_selected_vessel(self) -> RangeCheckResponse:
        return Util.find_in_range(self.vessels_ordered_by_mmsi, self.selected_vessel)

    def generate(self, from_: LatLongExpression, to: LatLongExpression, current_route_index: int, density: int = 5,
                 noise: float = 0.05, force_direction: (bool, bool) = (False, False)) -> list[Vessel]:
        current_vessels = []
        for _ in range(density):
            rand_point = Calculation.get_random_point(from_, to, noise, force_direction)
            generated_vessel_type = Simulation().generate_type()
            generated_vessel = Vessel(mmsi=Simulation().mmsi, course=rand_point[1],
                                      bearing=rand_point[1], heading=rand_point[1],
                                      distance_per_tick=generated_vessel_type.speed.value / self.tick_rate,
                                      position=rand_point[0],
                                      ais_range=generated_vessel_type.ais_range.value,
                                      ais_broadcast_interval=generated_vessel_type.ais_broadcast_interval.value,
                                      current_route_index=current_route_index if not rand_point[
                                          2] else current_route_index + 1,
                                      last_distance_to_current_mid_point_end=Calculation.calculate_distance(
                                          rand_point[0], to if not rand_point[2] else from_),
                                      vessel_type=generated_vessel_type.name, is_going_reverse_route=rand_point[2],
                                      dark_activity=False, is_removed=False)
            current_vessels.append(generated_vessel)
            self.vessels_ordered_by_mmsi.append(generated_vessel)
            Simulation().mmsi += 1
        return current_vessels

    def update_dark_activity_status(self, is_going_dark: bool, selected_dark_activity_vessel_mmsi: int):
        self.vessels_ordered_by_mmsi[
            selected_dark_activity_vessel_mmsi - self.mmsi_starting_number].dark_activity = is_going_dark

    def generate_type(self) -> VesselType:
        random_selected_type = random.choice(self.types)
        return random_selected_type
