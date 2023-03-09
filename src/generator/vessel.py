import random
import math
from generator.singleton import Singleton
EARTH_RADIUS = 6_371_000

class Vessel(metaclass=Singleton):

    def __init__(self):
        self.mmsi = 10000000
        self.vessels = []
        print('Vessels are generated')

    def generate(self, coordinates_1: list[float], coordinates_2: list[float], density: int = 5, noise: float = 0.05):
        
        for _ in range(density):
            current_vessels = []
            rand_point = Vessel.get_random_point(
                coordinates_1[0], coordinates_1[1], coordinates_2[0], coordinates_2[1], noise)
            Vessel().mmsi += 1
            metadata = {
                "mmsi": Vessel().mmsi,
                "course": rand_point[2],
                "heading": rand_point[2],
                "speed": random.random() * 200,
                "lon": rand_point[0],
                "lat": rand_point[1],
                "current_destination_lon": coordinates_2[0],
                "current_destination_lat": coordinates_2[1]
            }
            Vessel().vessels.append(metadata)
            current_vessels.append(metadata)
        return current_vessels

    def calculate_destination(distance, bearing, latitude, longitude):
        distance_over_radius = distance / EARTH_RADIUS
        latitude_differance = distance_over_radius * math.cos(bearing)
        destination_latitude = latitude + latitude_differance
        a_differance = math.log(math.tan(destination_latitude / 2 + math.pi / 4) / math.tan(latitude / 2 + math.pi / 4))
        q = latitude_differance / a_differance if abs(a_differance) > 10e-12 else math.cos(latitude) 

        longitude_differance = distance_over_radius * math.sin(bearing) / q
        destination_longitude = longitude + longitude_differance

        if abs(destination_latitude) > math.pi / 2:
            destination_latitude = math.pi - destination_latitude if destination_latitude > 0 else -1 * math.pi - destination_latitude

        return (destination_latitude, destination_longitude)

    def get_random_point(x1: float, y1: float, x2: float, y2: float, noise: float):
        diff_y = (y2 - y1)
        diff_x = (x2 - x1)

        rad = Vessel.calculate_bearing(math.radians(
            diff_x), math.radians(y1), math.radians(y2))
        deg = math.degrees(rad)

        slope = math.tan(rad)
        perpendicular_slope = -1 / slope
        perpendicular_slope_rad = math.atan(perpendicular_slope)

        rand_x = random.uniform(
            0, diff_x) if diff_x >= 0 else random.uniform(diff_x, 0)
        ratio = rand_x / diff_x
        final_x = x1 + rand_x
        final_y = y1 + (diff_y * ratio)

        hypothenuse = random.uniform(-noise, noise)
        noised_x = hypothenuse * math.sin(perpendicular_slope_rad) + final_x
        noised_y = hypothenuse * math.cos(perpendicular_slope_rad) + final_y
        return [noised_x, noised_y,  deg]

    # returns radian
    def calculate_bearing(diff_x: float, y1: float, y2: float):
        diff_x = math.radians(diff_x)
        y1, y2 = math.radians(y1), math.radians(y2)
        x = math.sin(diff_x) * math.cos(y2)
        y = math.cos(y1) * math.sin(y2) - math.sin(y1) * \
            math.cos(y2) * math.cos(diff_x)
        return math.atan2(x, y)
