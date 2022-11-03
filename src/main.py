from flask import Flask
import json
from generator import vessel

app = Flask("Dark Activity Detection")


@app.route("/vessels", methods=["GET"])
def get_ships():
    f = open('./src/data/routes.json')
    data = json.load(f)
    f.close()

    vessels = []
    for i in range(len(data)):
        coordinates = data[i]["coordinates"]
        for j in range(len(coordinates) - 1):
            cords = (coordinates[j], coordinates[j+1])
            vessels.append(vessel.Generator().generate(
                cords[0], cords[1], data[i]["density"][j], data[i]["noise"][j]))

    return vessels


@app.route("/ports", methods=["GET"])
def get_ports():
    f = open('./src/data/ports.json')
    data = json.load(f)
    f.close()
    return data
