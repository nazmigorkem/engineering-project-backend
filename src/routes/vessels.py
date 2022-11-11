import json
from generator.vessel import Generator
from fastapi import APIRouter
from typings.vessel import Vessel


router = APIRouter()
router.prefix = "/vessels"


class Vessels:

    @router.get("/get", response_model=list[list[Vessel]])
    def get():
        data = None
        with open('./data/ship_positions.json') as f:
            data = json.load(f)

        return data

    @router.get("/generate", response_model=list[list[Vessel]])
    def generate():
        data = None
        with open('./data/routes.json') as f:
            data = json.load(f)
        generator = Generator()
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
