from pydantic import BaseModel


class VesselType(BaseModel):
    mmsi: int
    course: float
    heading: float
    speed: float
    lon: float
    lat: float
