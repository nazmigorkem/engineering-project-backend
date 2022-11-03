import random
import math


class Generator:
    def __init__(self):
        pass

    def generate(self, coordinates_1: list[float], coordinates_2: list[float], density: float = 0.03):
        vessels = []
        for i in range(math.floor(1000 * density)):
            rand_point = self.get_rand_point(
                coordinates_1[0], coordinates_1[1], coordinates_2[0], coordinates_2[1])
            metadata = {
                "mmsi": 10000000 + i,
                "course": rand_point[2],
                "heading": rand_point[2],
                "speed": random.random() * 200,
                "lon": rand_point[0],
                "lat": rand_point[1],
            }
            vessels.append(metadata)
        return vessels

    def get_rand_point(self, x1: float, y1: float, x2: float, y2: float):
        diff_y = (y2 - y1)
        diff_x = (x2 - x1)

        deg = self.calculate_bearing(math.radians(
            diff_x), math.radians(y1), math.radians(y2))

        rand_x = random.uniform(0, abs(diff_x))
        ratio = (diff_x - rand_x) / diff_x
        final_x = x1 + rand_x
        final_y = y2 - (diff_y * ratio)

        noise_rand = random.uniform(0, 0.05)
        return [final_x + noise_rand, final_y + noise_rand, deg]

    def calculate_bearing(self, diff_x: float, y1: float, y2: float):
        diff_x = math.radians(diff_x)
        y1 = math.radians(y1)
        y2 = math.radians(y2)
        x = math.sin(diff_x) * math.cos(y2)
        y = math.cos(y1) * math.sin(y2) - math.sin(y1) * \
            math.cos(y2) * math.cos(diff_x)
        return math.degrees(math.atan2(x, y))
