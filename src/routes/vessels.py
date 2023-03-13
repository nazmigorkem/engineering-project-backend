import json
from lib.util import Util
from generator.vessel import Vessel
from fastapi import APIRouter
from typings.vessel import VesselType
import math

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
        Vessel().vessels = []
        return {
            "status": 200
        }


    @router.get("/generate")
    def generate():
        generator = Vessel()
        if len(Vessel().vessels) == 0: 
            
            data = None
            with open('./data/routes.json') as f:
                data = json.load(f)
            
            for x in data:
                coordinates = x["coordinates"]
                generator.vessels.append({
                    "from": x["from"],
                    "to": x["to"],
                    "route": coordinates,
                    "vessels": []
                })
                for (i, (f, s)) in enumerate(zip(coordinates[:-1], coordinates[1:])):
                    for y in generator.generate(f, s, i, x["density"][i], x["noise"][i]):
                        generator.vessels[-1]['vessels'].append(y)

            Util.dump('./data/ship_positions.json', generator.vessels)

            return generator.vessels
        else:

            Util.dump('./data/ship_positions.json', generator.vessels)
            for x in generator.vessels:
                for y in x['vessels']:

                    index = y['current_route_index']
                    current_destination = x['route'][index + 1]
                    distance = Vessel.calculate_distance(math.radians(current_destination[1]), math.radians(current_destination[0]), math.radians(y['lat']), math.radians(y['lon']))

                    if y["last_distance_to_current_mid_point_end"] < distance:
                        if len(x['route']) <= index + 2:
                            del y
                            continue
                        next_destination = x['route'][index + 2]
                        slope = Vessel.calculate_bearing(math.radians(next_destination[0] - current_destination[0]), math.radians(current_destination[1]), math.radians(next_destination[1]))
                        y['course'] = math.degrees(slope)
                        y['bearing'] = y['course']
                        current_destination = next_destination
                        y['current_route_index'] = index + 1
                        distance = Vessel.calculate_distance(math.radians(current_destination[1]), math.radians(current_destination[0]), math.radians(y['lat']), math.radians(y['lon']))
                    y["last_distance_to_current_mid_point_end"] = distance
                    
                    results = Vessel.calculate_destination(1000, math.radians(y['bearing']), math.radians(y['lat']), math.radians(y['lon']))
                    y['lat'] = results[0]
                    y['lon'] = results[1]
            return generator.vessels
