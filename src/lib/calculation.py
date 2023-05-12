import math
import random

from models.LatLong import LatLongExpression
EARTH_RADIUS = 6_371_000


class Calculation:
    @staticmethod
    def calculate_destination(distance: int | float, bearing: float, current_position: LatLongExpression) -> LatLongExpression:
        bearing = math.radians(bearing)
        distance_over_radius = distance / EARTH_RADIUS
        latitude_differance = distance_over_radius * math.cos(bearing)
        destination_latitude = current_position.latitude_in_radians + latitude_differance
        a_differance = math.log(math.tan(destination_latitude / 2 + math.pi / 4) / math.tan(current_position.latitude_in_radians / 2 + math.pi / 4))
        q = latitude_differance / a_differance if abs(a_differance) > 10e-12 else math.cos(current_position.latitude_in_radians)

        longitude_differance = distance_over_radius * math.sin(bearing) / q
        destination_longitude = current_position.longitude_in_radians + longitude_differance

        if abs(destination_latitude) > math.pi / 2:
            destination_latitude = math.pi - destination_latitude if destination_latitude > 0 else -1 * math.pi - destination_latitude
        return LatLongExpression(latitude_in_degrees=math.degrees(destination_latitude),
                                 latitude_in_radians=destination_latitude,
                                 longitude_in_degrees=math.degrees(destination_longitude),
                                 longitude_in_radians=destination_longitude)

    @staticmethod
    def calculate_distance(from_: LatLongExpression, to: LatLongExpression):
        latitude_differance = abs(from_.latitude_in_radians - to.latitude_in_radians)
        longitude_differance = abs(from_.longitude_in_radians - to.longitude_in_radians)

        a = math.sin(latitude_differance / 2) ** 2 + math.cos(from_.latitude_in_radians) * math.cos(to.latitude_in_radians) * math.sin(longitude_differance / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return EARTH_RADIUS * c

    @staticmethod
    def get_random_point(from_: LatLongExpression, to: LatLongExpression, noise: float) -> tuple[LatLongExpression, float, bool]:
        diff_y = (to.longitude_in_degrees - from_.longitude_in_degrees)
        diff_x = (to.latitude_in_degrees - from_.latitude_in_degrees)

        is_going_reverse_route = True if random.random() < 0.5 else False
        rad = Calculation.calculate_bearing(from_, to)
        deg = math.degrees(rad) + (180 if is_going_reverse_route else 0)

        slope = math.tan(rad)
        perpendicular_slope = -1 / slope
        perpendicular_slope_rad = math.atan(perpendicular_slope)

        rand_x = random.uniform(
            0, diff_x) if diff_x >= 0 else random.uniform(diff_x, 0)
        ratio = rand_x / diff_x
        final_x = from_.latitude_in_degrees + rand_x
        final_y = from_.longitude_in_degrees + (diff_y * ratio)

        hypotenuse = random.uniform(-noise, noise)
        noised_x = hypotenuse * math.sin(perpendicular_slope_rad) + final_x
        noised_y = hypotenuse * math.cos(perpendicular_slope_rad) + final_y
        return (LatLongExpression(latitude_in_degrees=noised_x,
                                  latitude_in_radians=math.radians(noised_x),
                                  longitude_in_degrees=noised_y,
                                  longitude_in_radians=math.radians(noised_y)),  deg, is_going_reverse_route)

    # returns radian
    @staticmethod
    def calculate_bearing(from_: LatLongExpression, to: LatLongExpression):
        diff_y = to.longitude_in_radians - from_.longitude_in_radians
        y = math.sin(diff_y) * math.cos(to.latitude_in_radians)
        x = math.cos(from_.latitude_in_radians) * math.sin(to.latitude_in_radians) - math.sin(from_.latitude_in_radians) * \
            math.cos(to.latitude_in_radians) * math.cos(diff_y)
        return math.atan2(y, x)
