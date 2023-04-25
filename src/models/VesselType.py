from dataclasses import dataclass


@dataclass
class ValueField:
    value: float | int
    unit: str


@dataclass
class VesselType:
    name: str
    length: ValueField
    speed: ValueField
    ais_range: ValueField
    ais_broadcast_interval: ValueField
