import json
from fastapi import APIRouter
from typings.vessel import VesselType, SelectedVessel
from typings.vessel import VesselType
from generator.simulation import Simulation
from generator.vessel import Vessel

router = APIRouter()
router.prefix = "/vessels"


class Vessels:
    generator = None

    @router.get("/get", response_model=list[list[VesselType]])
    def get():
        data = None
        with open('./data/ship_positions.json') as f:
            data = json.load(f)

        return data

    @router.post("/reset")
    def get():
        Vessel.clear()
        return {
            "status": 200
        }

    @router.post("/select")
    async def select(vessel: SelectedVessel):
        return Vessel().select_vessel(vessel.mmsi)

    @router.post("/generate")
    def generate(selectedVessel: VesselType = None):
        generator = Vessel()

        return Simulation.start_simulation(generator) if len(generator.vessels) == 0 else Simulation.next_tick(generator, selectedVessel);
