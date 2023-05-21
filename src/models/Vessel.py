from dataclasses import dataclass, asdict

from models.LatLong import LatLongExpression


@dataclass
class Vessel:
    mmsi: int
    position: LatLongExpression
    dark_activity: bool
    course: float
    heading: float
    bearing: float
    vessel_type: str
    distance_per_tick: float
    ais_range: float
    ais_broadcast_interval: int
    current_route_index: int
    is_going_reverse_route: bool
    last_distance_to_current_mid_point_end: float

    @property
    def __dict__(self):
        return asdict(self)
