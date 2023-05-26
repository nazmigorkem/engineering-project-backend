from fastapi import APIRouter

from lib.machine_learning import Detector
from lib.simulation import Simulation
from models.GenerateResponse import GenerateResponse
from models.RangeCheckResponse import RangeCheckResponse

router = APIRouter()
router.prefix = "/vessels"
detector_method = "ML"


class Vessels:

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
        simulation = Simulation(detector_method)
        simulation.detector.clear()
        simulation.selected_vessel = simulation.vessels_ordered_by_mmsi[selected_vessel_mmsi - simulation.mmsi_starting_number]
        return simulation.find_closest_vessels_of_selected_vessel()

    @staticmethod
    @router.post("/reset_selection")
    def select():
        Detector.clear()
        Simulation(detector_method).selected_vessel = None

    @staticmethod
    @router.post("/dark_activity")
    def dark_activity(is_dark_activity: bool, selected_vessel_mmsi_for_dark_activity: int):
        Simulation(detector_method).update_dark_activity_status(is_dark_activity, selected_vessel_mmsi_for_dark_activity)

    @staticmethod
    @router.post("/generate", response_model=GenerateResponse)
    def generate():
        simulation = Simulation(detector_method)

        return simulation.start_simulation() if not simulation.is_simulation_started else simulation.next_tick()
