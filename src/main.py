from flask import Flask
import json
app = Flask("Dark Activity Detection")


@app.route("/vessels", methods=["GET"])
def get_ships():
    f = open('./src/data/ship_positions.json')
    data = json.load(f)
    f.close()
    return data


@app.route("/ports", methods=["GET"])
def get_ports():
    f = open('./src/data/ports.json')
    data = json.load(f)
    f.close()
    return data
