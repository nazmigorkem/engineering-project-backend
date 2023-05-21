from fastapi import APIRouter

from lib.FSM import Detector
from lib.simulation import Simulation
from models.GenerateResponse import GenerateResponse
from models.RangeCheckResponse import RangeCheckResponse

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
        Simulation().selected_vessel = Simulation().vessels_ordered_by_mmsi[selected_vessel_mmsi - Simulation().mmsi_starting_number]
        return Simulation().find_closest_vessels_of_selected_vessel()

    @staticmethod
    @router.post("/reset_selection")
    def select():
        Detector.clear()
        Simulation().selected_vessel = None

    @staticmethod
    @router.post("/dark_activity")
    def dark_activity(is_dark_activity: bool, selected_vessel_mmsi_for_dark_activity: int):
        Simulation().update_dark_activity_status(is_dark_activity, selected_vessel_mmsi_for_dark_activity)

    @staticmethod
    @router.post("/generate", response_model=GenerateResponse)
    def generate():
        generator = Simulation()

        return Simulation().start_simulation() if not generator.is_simulation_started else Simulation().next_tick()
