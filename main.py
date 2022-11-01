from flask import Flask
import json
app = Flask("Dark Activity Detection")


@app.route("/vessels", methods=["GET"])
def hello_world():
    f = open('ship_positions.json')
    data = json.load(f)
    f.close()
    return data
