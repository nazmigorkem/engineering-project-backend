from dataclasses import dataclass


@dataclass
class Vessel:
    mmsi: int
    lat: float
    lon: float
    course: float
    heading: float
    bearing: float
    vessel_type: str
    distance_per_tick: float
    ais_range: float
    ais_broadcast_interval: int
    current_route_index: int
    last_distance_to_current_mid_point_end: float
