from generator.vessel import Vessel
from lib.calculation import Calculation
from lib.util import Util
import json
import math

class Simulation:
    @staticmethod
    def next_tick(generator, selected_vessel):
        closest = []
       
        # Vessel().vessels_ordered_by_latitude = []
        Util.dump('./data/ship_positions.json', generator.vessels)
        for x in generator.vessels:
            for y in x['vessels']:

                index = y['current_route_index']
                current_destination = x['route'][index + 1]
                distance = Calculation.calculate_distance(current_destination[1], current_destination[0], y['lat'], y['lon'])

                if y["last_distance_to_current_mid_point_end"] < distance:
                    if len(x['route']) <= index + 2:
                        del y
                        continue
                    next_destination = x['route'][index + 2]
                    slope = Calculation.calculate_bearing(math.radians(next_destination[0] - current_destination[0]), math.radians(current_destination[1]), math.radians(next_destination[1]))
                    y['course'] = math.degrees(slope)
                    y['bearing'] = y['course']
                    current_destination = next_destination
                    y['current_route_index'] = index + 1
                    distance = Calculation.calculate_distance(current_destination[1], current_destination[0], y['lat'], y['lon'])
                y["last_distance_to_current_mid_point_end"] = distance
                
                results = Calculation.calculate_destination(1000, math.radians(y['bearing']), math.radians(y['lat']), math.radians(y['lon']))
                y['lat'] = results[0]
                y['lon'] = results[1]
                # Util.insert_sorted(Vessel().vessels_ordered_by_latitude, y, "lat")
                if selected_vessel.mmsi != -1:
                    closest = Vessel().select_vessel(selected_vessel.mmsi)
        return {"generatedVessels": generator.vessels, "closestVessels": closest}


    @staticmethod
    def start_simulation(generator):
        data = None
        Vessel().selected_vessel = None
        with open('./data/routes.json') as f:
            data = json.load(f)
        
        for x in data:
            coordinates = x["coordinates"]
            generator.vessels.append({
                "route_id": x["route_id"],
                "from": x["from"],
                "to": x["to"],
                "route": coordinates,
                "vessels": []
            })
            for (i, (f, s)) in enumerate(zip(coordinates[:-1], coordinates[1:])):
                for y in generator.generate(f, s, i, x["density"][i], x["noise"][i]):
                    generator.vessels[-1]['vessels'].append(y)

        Util.dump('./data/ship_positions.json', generator.vessels)

        return {"generatedVessels": generator.vessels, "closestVessels": []}