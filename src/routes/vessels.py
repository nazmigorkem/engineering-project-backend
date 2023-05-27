from fastapi import APIRouter

from lib.FSM import Detector as FSMDetector
from lib.machine_learning import Detector as MLDetector
from lib.simulation import Simulation
from models.GenerateResponse import GenerateResponse
from models.RangeCheckResponse import RangeCheckResponse

router = APIRouter()
router.prefix = "/vessels"


class Vessels:

    @staticmethod
    @router.post("/reset")
    def get():
        Simulation.clear()
        FSMDetector.clear()
        MLDetector.clear()
        return {
            "status": 200
        }

    @staticmethod
    @router.post("/select", response_model=RangeCheckResponse)
    def select(selected_vessel_mmsi: int):
        simulation = Simulation()
        simulation.fsm_detector.clear()
        simulation.ml_detector.clear()
        simulation.selected_vessel = simulation.vessels_ordered_by_mmsi[selected_vessel_mmsi - simulation.mmsi_starting_number]
        return simulation.find_closest_vessels_of_selected_vessel()

    @staticmethod
    @router.post("/reset_selection")
    def select():
        FSMDetector.clear()
        MLDetector.clear()
        Simulation().selected_vessel = None

    @staticmethod
    @router.post("/dark_activity")
    def dark_activity(is_dark_activity: bool, selected_vessel_mmsi_for_dark_activity: int):
        Simulation().update_dark_activity_status(is_dark_activity, selected_vessel_mmsi_for_dark_activity)

    @staticmethod
    @router.post("/generate", response_model=GenerateResponse)
    def generate():
        simulation = Simulation()

        return simulation.start_simulation() if not simulation.is_simulation_started else simulation.next_tick()
