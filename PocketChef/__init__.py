from flask import Flask, render_template, request

import json
import time
import mysql.connector

app = Flask(__name__)

alive = 0
data = {}

def get_db():
    return mysql.connector.connect (
        host="localhost",
        user="pocketchef",
        password="KingClarke25#",
        database="pocketchefdb"
    )
@app.route("/test_db")
def test_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT 'DB connection OK'")
    result = cursor.fetchone()
    db.close()
    return str(result)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/meat_type_selector")
def meat_type_selector():
    return render_template("meat_type_selector.html")

@app.route("/cooking_session")
def cooking_session():
    image_url = request.args.get("image", "")  # Get the image URL from the query parameter
    return render_template("cooking_session.html", image_url=image_url)


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
