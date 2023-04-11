import random
import math
from generator.singleton import Singleton
from lib.util import Util
from lib.calculation import Calculation
POSSIBLE_TYPES = ["A"]

class Vessel(metaclass=Singleton):

    def __init__(self):
        self.mmsi_starting_number = 10_000_000
        self.mmsi = self.mmsi_starting_number
        self.vessels = []
        self.vessels_ordered_by_mmsi = []
        self.vessels_ordered_by_latitude = []
        self.selected_vessel = None
        print('Vessels are generated')

    def select_vessel(self, mmsi):
        self.selected_vessel = self.vessels_ordered_by_mmsi[mmsi - self.mmsi_starting_number]
        closest = Util.find_in_range(self.vessels_ordered_by_latitude, self.selected_vessel, 10 ** 4)
   
        return closest


    def generate(self, coordinates_1: list[float], coordinates_2: list[float], current_route_index, density: int = 5, noise: float = 0.05):
        
        for _ in range(density):
            current_vessels = []
            rand_point = Calculation.get_random_point(
                coordinates_1[0], coordinates_1[1], coordinates_2[0], coordinates_2[1], noise)
       
            metadata = {
                "mmsi": Vessel().mmsi,
                "course": rand_point[2],
                "bearing": rand_point[2],
                "heading": rand_point[2],
                "speed": random.random() * 200,
                "lon": rand_point[0],
                "lat": rand_point[1],
                "type_of_ship": POSSIBLE_TYPES[math.floor(random.random() * len(POSSIBLE_TYPES))],
                "current_route_index": current_route_index,
                "last_distance_to_current_mid_point_end": Calculation.calculate_distance(coordinates_2[1], coordinates_2[0], rand_point[1], rand_point[0])
            }
            current_vessels.append(metadata)
            self.vessels_ordered_by_mmsi.append(metadata)
            Util.insert_sorted(self.vessels_ordered_by_latitude, metadata, "lat")
            Vessel().mmsi += 1
        return current_vessels

 