from flask import Flask, render_template

import json
import time

app = Flask(__name__)

alive = 0
data = {}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/meat_type_selector")
def meat_type_selector():
    return render_template("meat_type_selector.html")

@app.route("/cooking_session.")
def cooking_session():
    return render_template("cooking_session.html")


@app.route("/keep_alive")
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data["keep_alive"] = keep_alive_count
    parsed_json = json.dumps(data)
    return str(parsed_json)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000, debug=True)
