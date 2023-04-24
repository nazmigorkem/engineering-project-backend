import math
import random
from lib.singleton import Singleton
from lib.util import Util
from lib.calculation import Calculation
import json


class Simulation(metaclass=Singleton):
    def __init__(self):
        with open('./data/vessel_types.json') as f:
            self.types = json.load(f)
        self.tick_rate = 60
        self.mmsi_starting_number = 10_000_000
        self.mmsi = self.mmsi_starting_number
        self.vessels = []
        self.vessels_ordered_by_mmsi = []
        self.selected_vessel = None
        print('Vessels are generated')

    def next_tick(self, selected_vessel):
        closest = []

        Util.dump('./data/ship_positions.json', self.vessels)
        for x in self.vessels:
            for y in x['vessels']:

                index = y['current_route_index']
                current_destination = x['route'][index + 1]
                distance = Calculation.calculate_distance(current_destination[1], current_destination[0], y['lat'],
                                                          y['lon'])

                if y["last_distance_to_current_mid_point_end"] < distance:
                    if len(x['route']) <= index + 2:
                        del y
                        continue
                    next_destination = x['route'][index + 2]
                    slope = Calculation.calculate_bearing(math.radians(next_destination[0] - current_destination[0]),
                                                          math.radians(current_destination[1]),
                                                          math.radians(next_destination[1]))
                    y['course'] = math.degrees(slope)
                    y['bearing'] = y['course']
                    current_destination = next_destination
                    y['current_route_index'] = index + 1
                    distance = Calculation.calculate_distance(current_destination[1], current_destination[0], y['lat'],
                                                              y['lon'])
                y["last_distance_to_current_mid_point_end"] = distance

                results = Calculation.calculate_destination(y["distance_per_tick"], math.radians(y['bearing']),
                                                            math.radians(y['lat']), math.radians(y['lon']))
                y['lat'] = results[0]
                y['lon'] = results[1]
                if selected_vessel.mmsi != -1:
                    closest = self.find_closest_vessels_of_selected_vessel(selected_vessel.mmsi)
        return {"generatedVessels": self.vessels, "closestVessels": closest}

    def start_simulation(self):
        with open('./data/routes.json') as f:
            data = json.load(f)

        for x in data:
            coordinates = x["coordinates"]
            self.vessels.append({
                "route_id": x["route_id"],
                "from": x["from"],
                "to": x["to"],
                "route": coordinates,
                "vessels": []
            })
            for (i, (f, s)) in enumerate(zip(coordinates[:-1], coordinates[1:])):
                for y in self.generate(f, s, i, x["density"][i], x["noise"][i]):
                    self.vessels[-1]['vessels'].append(y)

        Util.dump('./data/ship_positions.json', self.vessels)

        return {"generatedVessels": self.vessels, "closestVessels": []}

    def find_closest_vessels_of_selected_vessel(self, mmsi: int):
        self.selected_vessel = self.vessels_ordered_by_mmsi[mmsi - self.mmsi_starting_number]
        closest = Util.find_in_range(self.vessels_ordered_by_mmsi, self.selected_vessel)

        return closest

    def generate(self, coordinates_1: list[float], coordinates_2: list[float], current_route_index, density: int = 5,
                 noise: float = 0.05):
        current_vessels = []
        for _ in range(density):
            rand_point = Calculation.get_random_point(
                coordinates_1[0], coordinates_1[1], coordinates_2[0], coordinates_2[1], noise)
            generated_vessel_type = Simulation().generate_type()
            metadata = {
                "vessel_type": generated_vessel_type["name"],
                "mmsi": Simulation().mmsi,
                "course": rand_point[2],
                "bearing": rand_point[2],
                "heading": rand_point[2],
                "distance_per_tick": generated_vessel_type["speed"]["value"] / self.tick_rate,
                "lon": rand_point[0],
                "lat": rand_point[1],
                "aisRange": generated_vessel_type["aisRange"]["value"],
                "aisBroadcastInterval": generated_vessel_type["aisBroadcastInterval"]["value"],
                "current_route_index": current_route_index,
                "last_distance_to_current_mid_point_end": Calculation.calculate_distance(coordinates_2[1],
                                                                                         coordinates_2[0],
                                                                                         rand_point[1], rand_point[0])
            }
            current_vessels.append(metadata)
            self.vessels_ordered_by_mmsi.append(metadata)
            Simulation().mmsi += 1
        return current_vessels

    def generate_type(self):
        random_selected_type = random.choice(self.types["vesselTypes"])
        return random_selected_type
