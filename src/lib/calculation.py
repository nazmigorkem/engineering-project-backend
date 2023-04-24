import math
import random

EARTH_RADIUS = 6_371_000


class Calculation:
    @staticmethod
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
        return math.degrees(destination_latitude), math.degrees(destination_longitude)

    @staticmethod
    def calculate_distance(latitude_1, longitude_1, latitude_2, longitude_2):
        latitude_1 = math.radians(latitude_1)
        latitude_2 = math.radians(latitude_2)
        longitude_1 = math.radians(longitude_1)
        longitude_2 = math.radians(longitude_2)
        latitude_differance = abs(latitude_1 - latitude_2)
        longitude_differance = abs(longitude_1 - longitude_2)

        a = math.sin(latitude_differance / 2) ** 2 + math.cos(latitude_1) * math.cos(latitude_2) * math.sin(longitude_differance / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return EARTH_RADIUS * c

    @staticmethod
    def get_random_point(x1: float, y1: float, x2: float, y2: float, noise: float):
        diff_y = (y2 - y1)
        diff_x = (x2 - x1)

        rad = Calculation.calculate_bearing(math.radians(
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

        hypotenuse = random.uniform(-noise, noise)
        noised_x = hypotenuse * math.sin(perpendicular_slope_rad) + final_x
        noised_y = hypotenuse * math.cos(perpendicular_slope_rad) + final_y
        return [noised_x, noised_y,  deg]

    # returns radian
    @staticmethod
    def calculate_bearing(diff_x: float, y1: float, y2: float):
        diff_x = math.radians(diff_x)
        y1, y2 = math.radians(y1), math.radians(y2)
        x = math.sin(diff_x) * math.cos(y2)
        y = math.cos(y1) * math.sin(y2) - math.sin(y1) * \
            math.cos(y2) * math.cos(diff_x)
        return math.atan2(x, y)
