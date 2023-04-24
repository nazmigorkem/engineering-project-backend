from pydantic import BaseModel

class VesselType(BaseModel):
    mmsi: int
    course: float
    heading: float
    distance_per_tick: float
    aisRange: int
    lon: float
    lat: float


class SelectedVessel(BaseModel):
    mmsi: int
    route_id: int


