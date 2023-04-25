from dataclasses import dataclass
from models.LatLong import LatLongExpression


@dataclass
class Vessel:
    mmsi: int
    position: LatLongExpression
    course: float
    heading: float
    bearing: float
    vessel_type: str
    distance_per_tick: float
    ais_range: float
    ais_broadcast_interval: int
    current_route_index: int
    last_distance_to_current_mid_point_end: float
