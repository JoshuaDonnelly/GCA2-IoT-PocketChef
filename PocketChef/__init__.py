from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from dotenv import load_dotenv
import os

load_dotenv()

import json
import time
import mysql.connector
from authlib.integrations.flask_client import OAuth
from functools import wraps

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    pubsub = os.getenv("PUBNUB_SUBSCRIBE_KEY")
    alive = 0
    data = {}
    
    # OAuth setup, "Kwargs" basically an object of parameters (name, picture, etc.)
    oauth = OAuth(app)
    google = oauth.register(
        name='google',
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )
    
    # Login required decorator, takes parameters and checks if user is logged in
    # Allows us to use @login_required on routes
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

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
        user = session.get('user')
        return render_template("index.html", user=user)

    @app.route("/meat_type_selector")
    def meat_type_selector():
        meat_type = request.args.get("type", "chicken")
        user = session.get('user')
        return render_template("meat_type_selector.html", meat_type=meat_type, user=user)

    @app.route("/cooking_session")
    def cooking_session():
        image_url = request.args.get("image", "")
        meat_name = request.args.get("name", "Meat")
        user = session.get('user')
        return render_template("cooking_session.html", image_url=image_url, meat_name=meat_name, user=user)
    
    @app.route("/recipes")
    def recipes():
        user = session.get('user')
        return render_template("recipes.html", user=user)
    
    @app.route("/login")
    def login():
        redirect_uri = url_for('authorize', _external=True)
        return google.authorize_redirect(redirect_uri)

    @app.route("/login/callback")
    def authorize():
        try:
            token = google.authorize_access_token()
            user_info = token.get('userinfo')
            if user_info:
                session['user'] = {
                    'email': user_info['email'],
                    'name': user_info.get('name', ''),
                    'picture': user_info.get('picture', '')
                }
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Login error: {e}")
            return redirect(url_for('index'))

    @app.route("/logout")
    def logout():
        session.pop('user', None)
        return redirect(url_for('index'))

    @app.route("/pubnub_config")
    def pubnub_config():
        config = {
            "subscribe_key": pubsub,
            "channel": "raspi"
        }
        return json.dumps(config)

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
