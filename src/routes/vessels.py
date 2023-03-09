import json
from generator.vessel import Vessel
from fastapi import APIRouter
from typings.vessel import VesselType


router = APIRouter()
router.prefix = "/vessels"


class Vessels:

    @router.get("/get", response_model=list[list[VesselType]])
    def get():
        data = None
        with open('./data/ship_positions.json') as f:
            data = json.load(f)

        return data

    @router.get("/generate")
    def generate():
        data = None
        with open('./data/routes.json') as f:
            data = json.load(f)
        generator = Vessel()

        list = []
        for x in data:
            coordinates = x["coordinates"]
            list.append({
                "from": x["from"],
                "to": x["to"],
                "end_points": [x["coordinates"][0], x["coordinates"][-1]],
                "vessels": []
            })
            for (i, (f, s)) in enumerate(zip(coordinates[:-1], coordinates[1:])):
                for y in generator.generate(f, s, x["density"][i], x["noise"][i]):
                    list[-1]['vessels'].append(y)

        json_dump = json.dumps(list, indent=2)
        with open("./data/ship_positions.json", "w") as out_f:
            out_f.write(json_dump)

        return list
    
    @router.get("/update", response_model=list[list[VesselType]])
    def update():
        data = None
        with open('./data/ship_positions.json') as f:
            data = json.load(f)
        generator = Vessel()
        vessels = []
        for x in data:
            coordinates = x["coordinates"]
            for (i, (f, s)) in enumerate(zip(coordinates[:-1], coordinates[1:])):
                vessels.append(generator.generate(
                    f, s, x["density"][i], x["noise"][i]))

        json_dump = json.dumps(vessels, indent=2)

        with open("./data/ship_positions.json", "w") as out_f:
            out_f.write(json_dump)

        return vessels
