from flask import Flask
import json
from generator.vessel import Generator

app = Flask("Dark Activity Detection")


@app.route("/vessels", methods=["GET"])
def get_ships():
    data = None
    with open('./src/data/routes.json') as f:
        data = json.load(f)

    vessels = []
    for x in data:
        coordinates = x["coordinates"]
        for (i, (f, s)) in enumerate(zip(coordinates[:-1], coordinates[1:])):
            vessels.append(Generator().generate(
                f, s, x["density"][i], x["noise"][i]))

    return vessels


@app.route("/ports", methods=["GET"])
def get_ports():
    data = None
    with open('./src/data/ports.json') as f:
        data = json.load(f)
    return data


@app.route("/routes", methods=["GET"])
def get_routes():
    data = None
    with open('./src/data/routes.json') as f:
        data = json.load(f)
    return data
