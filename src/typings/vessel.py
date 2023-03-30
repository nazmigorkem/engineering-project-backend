from pydantic import BaseModel


class VesselType(BaseModel):
    mmsi: int
    course: float
    heading: float
    speed: float
    lon: float
    lat: float

class SelectedVessel(BaseModel):
    mmsi: int
    route_id: int
