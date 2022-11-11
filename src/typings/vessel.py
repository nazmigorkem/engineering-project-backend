from pydantic import BaseModel


class Vessel(BaseModel):
    mmsi: int
    course: float
    heading: float
    speed: float
    lon: float
    lat: float
