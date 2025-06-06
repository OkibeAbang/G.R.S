import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [title, setTitle] = useState("");
  const [recs, setRecs] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);


  const fetchRecommendations = async () => {
    if (!title.trim()) return;

    setLoading(true);

    try {
      const response = await axios.get(`http://127.0.0.1:5000/recommend_by_game?title=${encodeURIComponent(title)}`);
      if (response.data.error) {
        setError(response.data.error);
        setRecs([]);
      } else {
        setRecs(response.data.recommendations);
        setError("");
      }
    } catch (err) {
      console.error(err);
      setError("Failed to fetch recommendations. Please try again later.");
      setRecs([]);
    }
    setLoading(false)
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") fetchRecommendations();
  };

  return (
    <div className="App">
      <h1>🎮 Game Recommendation System</h1>

      <div className="search-bar">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Enter a game title (e.g., Hollow Knight)"
        />
        <button onClick={fetchRecommendations}>Get Recommendations</button>
      </div>

      {error && <p className="error-msg">{error}</p>}

      {loading && <div className="spinner"></div>}


      <div className="recommendation-grid">
        {recs.map((rec, index) => (
          <div key={index} className="game-card">
            <img
              src={rec.cover_url || "https://via.placeholder.com/150x200?text=No+Image"}
              alt={rec.game}
            />
            <strong>{rec.game}</strong>
            <p>Similarity: {rec.similarity}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
