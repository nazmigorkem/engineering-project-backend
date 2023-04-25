import json
import math
import random

from lib.calculation import Calculation
from lib.singleton import Singleton
from lib.util import Util
from lib.FSM import Detector
from models.Route import Route
from models.Vessel import Vessel
from models.GenerateResponse import GenerateResponse
from models.VesselType import VesselType, ValueField
from models.LatLong import LatLongExpression


class Simulation(metaclass=Singleton):
    def __init__(self):
        self.types: list[VesselType] = []
        self.routes: list[Route] = []

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
                                         ais_broadcast_interval=ValueField(value=ais_broadcast_interval["value"], unit=ais_broadcast_interval["unit"])))

        with open('./data/routes.json') as f:
            raw_route_data = json.load(f)
        for raw_route in raw_route_data:
            coordinates = raw_route["coordinates"]
            lat_long_expressions: list[LatLongExpression] = []
            for coordinate in coordinates:
                lat_long_expressions.append(LatLongExpression(latitude_in_degrees=coordinate[0], latitude_in_radians=math.radians(coordinate[0]),
                                                              longitude_in_degrees=coordinate[1], longitude_in_radians=math.radians(coordinate[1])))
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
        self.selected_vessel = None
        self.is_simulation_started = False
        print('Vessels are generated')

    def next_tick(self, selected_vessel) -> GenerateResponse:
        closest = []

        for route in self.routes:
            for vessel in route.vessels:
                vessel: Vessel = vessel
                index = vessel.current_route_index
                current_destination = route.coordinates[index + 1]
                distance = Calculation.calculate_distance(current_destination, vessel.position)

                if vessel.last_distance_to_current_mid_point_end < distance:
                    if not vessel.is_going_reverse_route and len(route.coordinates) <= index + 2:
                        del vessel
                        continue
                    elif vessel.is_going_reverse_route and index - 2 <= 0:
                        del vessel
                        continue
                    next_destination = route.coordinates[index + 2 if not vessel.is_going_reverse_route else index - 2]
                    slope = Calculation.calculate_bearing(current_destination, next_destination)
                    vessel.course = math.degrees(slope)
                    vessel.bearing = vessel.course
                    current_destination = next_destination
                    vessel.current_route_index = index + 1 if not vessel.is_going_reverse_route else index - 1
                    distance = Calculation.calculate_distance(current_destination, vessel.position)
                vessel.last_distance_to_current_mid_point_end = distance

                vessel.position = Calculation.calculate_destination(vessel.distance_per_tick, vessel.bearing, vessel.position)
                if selected_vessel.mmsi != -1:
                    closest = self.find_closest_vessels_of_selected_vessel(selected_vessel.mmsi)
                    Detector(closest_vessels=closest, selected_vessel=selected_vessel).next_state(closest)

        return GenerateResponse(self.routes, closest)

    def start_simulation(self) -> GenerateResponse:
        for (ith_route, route) in enumerate(self.routes):
            for (i, (from_, to)) in enumerate(zip(route.coordinates[:-1], route.coordinates[1:])):
                for y in self.generate(from_, to, i, route.density[i], route.noise[i]):
                    self.routes[ith_route].vessels.append(y)
        self.is_simulation_started = True
        return GenerateResponse(self.routes, [])

    def find_closest_vessels_of_selected_vessel(self, mmsi: int) -> list[Vessel]:
        self.selected_vessel = self.vessels_ordered_by_mmsi[mmsi - self.mmsi_starting_number]
        closest = Util.find_in_range(self.vessels_ordered_by_mmsi, self.selected_vessel)

        return closest

    def generate(self, from_: LatLongExpression, to: LatLongExpression, current_route_index, density: int = 5, noise: float = 0.05) -> list[Vessel]:
        current_vessels = []
        for _ in range(density):
            rand_point = Calculation.get_random_point(from_, to, noise)
            generated_vessel_type = Simulation().generate_type()
            generated_vessel = Vessel(mmsi=Simulation().mmsi, course=rand_point[1],
                                      bearing=rand_point[1], heading=rand_point[1],
                                      distance_per_tick=generated_vessel_type.speed.value / self.tick_rate,
                                      position=rand_point[0],
                                      ais_range=generated_vessel_type.ais_range.value,
                                      ais_broadcast_interval=generated_vessel_type.ais_broadcast_interval.value,
                                      current_route_index=current_route_index,
                                      last_distance_to_current_mid_point_end=Calculation.calculate_distance(rand_point[0], to),
                                      vessel_type=generated_vessel_type.name, is_going_reverse_route=rand_point[2])
            current_vessels.append(generated_vessel)
            self.vessels_ordered_by_mmsi.append(generated_vessel)
            Simulation().mmsi += 1
        return current_vessels

    def generate_type(self) -> VesselType:
        random_selected_type = random.choice(self.types)
        return random_selected_type
