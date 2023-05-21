import json
import random

from lib.FSM import Detector
from lib.simulation import Simulation
from models.LogData import LogData
from models.Vessel import Vessel

simulation = Simulation()
simulation.start_simulation()
logs: list[dict[str, any]] = []
for i in range(50):
    if i % 10 == 0 or simulation.selected_vessel is None:
        Detector.clear()
        simulation.selected_vessel = random.choice(simulation.vessels_ordered_by_mmsi)
    closest_vessels = simulation.find_closest_vessels_of_selected_vessel(simulation.selected_vessel.mmsi)

    dark_activity_vessel: Vessel = random.choice(simulation.vessels_ordered_by_mmsi)
    if dark_activity_vessel != simulation.selected_vessel:
        dark_activity_vessel.dark_activity = True

    current_tick = simulation.next_tick()
    current_vessels: list[Vessel] = []
    for x in current_tick.generated_vessels:
        current_vessels.extend(x.vessels)
    logs.append(LogData(i, current_vessels, current_tick.range_check).__dict__)

logs.append({"total_dark_activities": list(map(lambda y: y.__dict__, simulation.total_dark_activity_for_whole_simulation))})

with open("output.json", "w") as outfile:
    outfile.write(json.dumps(logs, indent=4))
