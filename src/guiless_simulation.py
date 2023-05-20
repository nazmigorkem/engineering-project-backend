from lib.simulation import Simulation
from models.RangeCheckResponse import RangeCheckResponse
from models.Vessel import Vessel
from models.GenerateResponse import GenerateResponse
from models.LogData import LogData
import json

simulation = Simulation()
simulation.start_simulation()
logs: list[dict[str, any]] = []
for i in range(100):
    current_tick = simulation.next_tick()
    current_vessels: list[Vessel] = []
    for x in current_tick.generated_vessels:
        current_vessels.extend(x.vessels)
    logs.append(LogData(i, current_vessels, current_tick.range_check, current_tick.total_dark_activity_vessels).__dict__)


with open("output.json", "w") as outfile:
    outfile.write(json.dumps(logs, indent=4))
