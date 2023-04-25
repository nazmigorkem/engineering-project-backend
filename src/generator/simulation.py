import json
import math
import random

from lib.calculation import Calculation
from lib.singleton import Singleton
from lib.util import Util
from models.Route import Route
from models.Vessel import Vessel
from models.GenerateResponse import GenerateResponse


class Simulation(metaclass=Singleton):
    def __init__(self):
        with open('./data/vessel_types.json') as f:
            self.types = json.load(f)
        self.tick_rate = 60
        self.mmsi_starting_number = 10_000_000
        self.mmsi = self.mmsi_starting_number
        self.routes: list[Route] = []
        self.vessels_ordered_by_mmsi: list[Vessel] = []
        self.selected_vessel = None
        print('Vessels are generated')

    def next_tick(self, selected_vessel):
        closest = []

        for route in self.routes:
            for vessel in route.vessels:
                vessel: Vessel = vessel
                index = vessel.current_route_index
                current_destination = route.coordinates[index + 1]
                distance = Calculation.calculate_distance(current_destination[1], current_destination[0], vessel.lat,
                                                          vessel.lon)

                if vessel.last_distance_to_current_mid_point_end < distance:
                    if len(route.coordinates) <= index + 2:
                        del vessel
                        continue
                    next_destination = route.coordinates[index + 2]
                    slope = Calculation.calculate_bearing(next_destination[0] - current_destination[0],
                                                          current_destination[1],
                                                          next_destination[1])
                    vessel.course = math.degrees(slope)
                    vessel.bearing = vessel.course
                    current_destination = next_destination
                    vessel.current_route_index = index + 1
                    distance = Calculation.calculate_distance(current_destination[1], current_destination[0], vessel.lat,
                                                              vessel.lon)
                vessel.last_distance_to_current_mid_point_end = distance

                results = Calculation.calculate_destination(vessel.distance_per_tick, vessel.bearing,
                                                            vessel.lat, vessel.lon)
                vessel.lat = results[0]
                vessel.lon = results[1]
                if selected_vessel.mmsi != -1:
                    closest = self.find_closest_vessels_of_selected_vessel(selected_vessel.mmsi)

        return GenerateResponse(self.routes, closest)

    def start_simulation(self):
        with open('./data/routes.json') as f:
            data = json.load(f)

        for raw_route in data:
            coordinates = raw_route["coordinates"]
            route = Route(route_id=raw_route["route_id"],
                          _from=raw_route["from"],
                          to=raw_route["to"],
                          coordinates=coordinates,
                          vessels=[],
                          density=raw_route["density"], noise=raw_route["noise"])
            self.routes.append(route)
            for (i, (f, s)) in enumerate(zip(coordinates[:-1], coordinates[1:])):
                for y in self.generate(f, s, i, route.density[i], route.noise[i]):
                    self.routes[-1].vessels.append(y)

        return GenerateResponse(self.routes, [])

    def find_closest_vessels_of_selected_vessel(self, mmsi: int):
        self.selected_vessel = self.vessels_ordered_by_mmsi[mmsi - self.mmsi_starting_number]
        closest = Util.find_in_range(self.vessels_ordered_by_mmsi, self.selected_vessel)

        return closest

    def generate(self, coordinates_1: list[float], coordinates_2: list[float], current_route_index, density: int = 5, noise: float = 0.05):
        current_vessels = []
        for _ in range(density):
            rand_point = Calculation.get_random_point(coordinates_1[0], coordinates_1[1], coordinates_2[0], coordinates_2[1], noise)
            generated_vessel_type = Simulation().generate_type()
            generated_vessel = Vessel(mmsi=Simulation().mmsi, course=rand_point[2],
                                      bearing=rand_point[2], heading=rand_point[2],
                                      distance_per_tick=generated_vessel_type["speed"]["value"] / self.tick_rate,
                                      lat=rand_point[1], lon=rand_point[0],
                                      ais_range=generated_vessel_type["aisRange"]["value"],
                                      ais_broadcast_interval=generated_vessel_type["aisBroadcastInterval"]["value"],
                                      current_route_index=current_route_index,
                                      last_distance_to_current_mid_point_end=Calculation.calculate_distance(
                                          coordinates_2[1],
                                          coordinates_2[0],
                                          rand_point[1], rand_point[0]),
                                      vessel_type=generated_vessel_type["name"])
            current_vessels.append(generated_vessel)
            self.vessels_ordered_by_mmsi.append(generated_vessel)
            Simulation().mmsi += 1
        return current_vessels

    def generate_type(self):
        random_selected_type = random.choice(self.types["vesselTypes"])
        return random_selected_type
