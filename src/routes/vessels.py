import json
from fastapi import APIRouter
from typings.vessel import VesselType, SelectedVessel
from generator.simulation import Simulation

router = APIRouter()
router.prefix = "/vessels"


class Vessels:
    generator = None

    @staticmethod
    @router.get("/get", response_model=list[list[VesselType]])
    def get():
        with open('./data/ship_positions.json') as f:
            data = json.load(f)

        return data

    @staticmethod
    @router.post("/reset")
    def get():
        Simulation.clear()
        return {
            "status": 200
        }

    @staticmethod
    @router.post("/select")
    async def select(vessel: SelectedVessel):
        return Simulation().find_closest_vessels_of_selected_vessel(vessel.mmsi)

    @staticmethod
    @router.post("/generate")
    def generate(selected_vessel: VesselType = None):
        generator = Simulation()
        return Simulation().start_simulation() if len(generator.vessels) == 0 else Simulation().next_tick(selected_vessel)
