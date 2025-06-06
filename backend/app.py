from flask import Flask, jsonify, request
from flask_cors import CORS
from recommender import get_mock_recommendations, get_game_recommendations
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from db import init_db
import sqlite3
init_db()


app = Flask(__name__)

CORS(app)  # <-- This allows frontend to talk to backend


@app.route("/")
def home():
    return "🎮 Welcome to the Game Recommendation API!"

@app.route("/recommend", methods=["GET"])
def recommend():
    user_id = request.args.get("user_id", default=1, type=int)
    return jsonify(get_mock_recommendations(user_id))

@app.route("/recommend_by_game", methods=["GET"])
def recommend_by_game():
    title = request.args.get("title")
    if not title:
        return jsonify({"error": "Please provide a game title like ?title=Hades"}), 400
    return jsonify(get_game_recommendations(title))

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    hashed_pw = generate_password_hash(password)

    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        conn.close()
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409



@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return jsonify({"error": "User not found"}), 404

    hashed_password = result[0]

    if check_password_hash(hashed_password, password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid password"}), 401


if __name__ == "__main__":
    app.run(debug=True)
