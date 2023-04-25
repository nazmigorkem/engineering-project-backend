from fastapi import APIRouter
from generator.simulation import Simulation
from models.Vessel import Vessel
from models.SelectedVessel import SelectedVessel
from models.GenerateResponse import GenerateResponse


router = APIRouter()
router.prefix = "/vessels"


class Vessels:
    generator = None

    @staticmethod
    @router.post("/reset")
    def get():
        Simulation.clear()
        return {
            "status": 200
        }

    @staticmethod
    @router.post("/select", response_model=list[Vessel])
    async def select(vessel: SelectedVessel):
        return Simulation().find_closest_vessels_of_selected_vessel(vessel.mmsi)

    @staticmethod
    @router.post("/generate", response_model=GenerateResponse)
    def generate(selected_vessel: Vessel = None):
        generator = Simulation()

        return Simulation().start_simulation() if len(generator.routes) == 0 else Simulation().next_tick(selected_vessel)
