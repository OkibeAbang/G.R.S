from flask import Flask, jsonify, request
from flask_cors import CORS
from recommender import get_mock_recommendations, get_game_recommendations


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

if __name__ == "__main__":
    app.run(debug=True)
