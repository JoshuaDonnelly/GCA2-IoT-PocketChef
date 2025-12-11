from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

import json
import time
import mysql.connector

def create_app():
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
    
    @app.route("/recipes")
    def recipes():
        return render_template("recipes.html")

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
        nonlocal alive, data
        alive += 1
        keep_alive_count = str(alive)
        data["keep_alive"] = keep_alive_count
        parsed_json = json.dumps(data)
        return str(parsed_json)

    # Import and register database routes
    from .db import init_db_pool, save_cooking_session, list_sessions
    init_db_pool()

    @app.route("/api/cooking_sessions", methods=["POST"])
    def api_create_session():
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        if not data.get("device_id"):
            return jsonify({"error": "device_id required"}), 400

        try:
            inserted_id = save_cooking_session(data)
        except Exception as e:
            app.logger.exception("Failed to save session")
            return jsonify({"error": "server error"}), 500

        return jsonify({"id": inserted_id}), 201

    @app.route("/api/cooking_sessions", methods=["GET"])
    def api_list_sessions():
        limit = int(request.args.get("limit", 50))
        offset = int(request.args.get("offset", 0))
        rows = list_sessions(limit=limit, offset=offset)
        return jsonify(rows)

    return app

# Create app instance
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
