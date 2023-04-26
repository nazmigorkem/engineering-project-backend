from fastapi import APIRouter
from lib.simulation import Simulation
from models.RangeCheckResponse import RangeCheckResponse
from models.Vessel import Vessel
from models.GenerateResponse import GenerateResponse
from lib.FSM import Detector

router = APIRouter()
router.prefix = "/vessels"


class Vessels:
    generator = None

    @staticmethod
    @router.post("/reset")
    def get():
        Simulation.clear()
        Detector.clear()
        return {
            "status": 200
        }

    @staticmethod
    @router.post("/select", response_model=RangeCheckResponse)
    def select(selected_vessel_mmsi: int):
        Detector.clear()
        return Simulation().find_closest_vessels_of_selected_vessel(selected_vessel_mmsi)

    @staticmethod
    @router.post("/dark_activity")
    def dark_activity(is_dark_activity: bool, selected_vessel_mmsi_for_dark_activity: int):
        print(is_dark_activity, selected_vessel_mmsi_for_dark_activity)
        Simulation().update_dark_activity_status(is_dark_activity, selected_vessel_mmsi_for_dark_activity)

    @staticmethod
    @router.post("/generate", response_model=GenerateResponse)
    def generate(selected_vessel: Vessel = None):
        generator = Simulation()

        return Simulation().start_simulation() if not generator.is_simulation_started else Simulation().next_tick(selected_vessel)
