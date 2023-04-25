from dataclasses import dataclass
from models.Vessel import Vessel
from models.Route import Route


@dataclass
class GenerateResponse:
    generated_vessels: list[Route]
    closest_vessels: list[Vessel]
