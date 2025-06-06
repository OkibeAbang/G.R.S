import pandas as pd
import requests
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

RAWG_API_KEY = "d682cc6ecf1d43beae83e5052bb9ee6e"
RAWG_BASE_URL = "https://api.rawg.io/api/games"

DATA_PATH = os.path.join("data", "steam.csv")

# Load dataset
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    df = pd.DataFrame()

# Clean and prepare TF-IDF
def preprocess():
    # Cleaning up the data (removing missing missing values and avoiding duplicates)
    df.dropna(subset=["name", "genres"], inplace=True)
    df.drop_duplicates(subset=["name"], inplace=True)

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df["genres"])  # You can use "short_description" if available
    
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df.index, index=df["name"]).drop_duplicates()
    
    return df, cosine_sim, indices

df, cosine_sim, indices = preprocess()


def get_game_cover(title):
    params = {
        "search": title,
        "key": RAWG_API_KEY
    }
    try:
        response = requests.get(RAWG_BASE_URL, params=params)
        results = response.json().get("results", [])
        if results:
            return results[0].get("background_image", "")
    except:
        return ""
    return ""

# Get recommendations
def get_game_recommendations(title, num=5):
    if title not in indices:
        return {"error": "Game not found."}

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num+1]
    game_indices = [i[0] for i in sim_scores]

    return {
        "input_game": title,
        "recommendations": [
            {"game": df.iloc[i]["name"], "cover_url": get_game_cover(df.iloc[i]["name"])}
            for j, i in enumerate(game_indices)
        ]
    }



# For testing
def get_mock_recommendations(user_id):
    return get_game_recommendations("Counter-Strike", 5)
