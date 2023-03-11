import json
from lib.util import Util
from generator.vessel import Vessel
from fastapi import APIRouter
from typings.vessel import VesselType


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

    @router.get("/generate")
    def generate():
        generator = Vessel()
        data = None
        print(len(Vessel().vessels))
        if len(Vessel().vessels) == 0: 
            
            with open('./data/routes.json') as f:
                data = json.load(f)
            
            for x in data:
                coordinates = x["coordinates"]
                generator.vessels.append({
                    "from": x["from"],
                    "to": x["to"],
                    "end_points": [x["coordinates"][0], x["coordinates"][-1]],
                    "vessels": []
                })
                for (i, (f, s)) in enumerate(zip(coordinates[:-1], coordinates[1:])):
                    for y in generator.generate(f, s, x["density"][i], x["noise"][i]):
                        generator.vessels[-1]['vessels'].append(y)

            Util.dump('./data/ship_positions.json', generator.vessels)

            return generator.vessels
        else:

            Util.dump('./data/ship_positions.json', generator.vessels)
    
            return generator.vessels
