from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

import json
import time
import mysql.connector

app = Flask(__name__)

alive = 0
data = {}

def get_db():
    return mysql.connector.connect (
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
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
    image_url = request.args.get("image", "")
    try:
        with open("latest_temp.json") as f:
            temp_data = json.load(f)
    except Exception:
        temp_data = {"temperature": "N/A"}
    return render_template("cooking_session.html", image_url=image_url, temp_data=temp_data)

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

from .db import init_db_pool, save_cooking_session, list_sessions

init_db_pool()

@app.route("/api/cooking_sessions", methods=["POST"])
def api_create_session():
    """
    Expects JSON body:
    {
      "device_id":"pi-01",
      "meat_type":"beef",
      "target_temp": 75.0,
      "actual_temp": 72.3,
      "start_time": "2025-11-23 12:00:00",
      "end_time": "2025-11-23 12:25:00",
      "notes": "seared"
    }
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    # Basic validation
    if not data.get("device_id"):
        return jsonify({"error": "device_id required"}), 400

    # Normalize/convert fields where appropriate (float/datetime sanitising)
    try:
        # optionally parse/validate datetimes here
        inserted_id = save_cooking_session(data)
    except Exception as e:
        # log exception server-side - don't leak details to client
        app.logger.exception("Failed to save session")
        return jsonify({"error": "server error"}), 500

    return jsonify({"id": inserted_id}), 201

@app.route("/api/cooking_sessions", methods=["GET"])
def api_list_sessions():
    limit = int(request.args.get("limit", 50))
    offset = int(request.args.get("offset", 0))
    rows = list_sessions(limit=limit, offset=offset)
    return jsonify(rows)
