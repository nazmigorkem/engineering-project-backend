from dataclasses import dataclass


@dataclass
class SelectedVessel:
    mmsi: int
    route_id: int
