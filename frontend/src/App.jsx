import React, { useState } from "react";
import axios from "axios";

function App() {
  const [movie, setMovie] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setRecommendations([]);
    setLoading(true);

    try {
      const trimmedMovie = movie.trim();
      if (!trimmedMovie) {
        setError("Please enter a movie name.");
        setLoading(false);
        return;
      }

      const res = await axios.post("http://127.0.0.1:5000/recommend", {
         movie: trimmedMovie,
      });

      if (res.data.error) {
        setError(res.data.error);
      } else {
        setRecommendations(res.data.recommendations);
      }
    } catch (err) {
      setError("Server error. Please try again later.");
    }

    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white px-4">
      <h1 className="text-3xl font-bold mb-6 text-center">
        🎬 Movie Recommendation System
      </h1>

      <form
        onSubmit={handleSubmit}
        className="flex flex-col sm:flex-row gap-3 w-full max-w-md"
      >
        <input
          type="text"
          value={movie}
          onChange={(e) => setMovie(e.target.value)}
          placeholder="Enter a movie name (e.g., Avatar)"
          className="flex-1 text-white px-4 py-2 rounded-lg text-black"
          required
        />
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg font-semibold"
        >
          {loading ? "Loading..." : "Recommend"}
        </button>
      </form>

      {error && <p className="mt-4 text-red-400">{error}</p>}

      {recommendations.length > 0 && (
        <div className="mt-8 w-full max-w-md">
          <h2 className="text-xl font-semibold mb-3 text-center">
            Recommended Movies:
          </h2>
          <div className="bg-gray-800 p-4 rounded-lg shadow-lg">
            <ul className="space-y-2">
              {recommendations.map((r, index) => (
                <li
                  key={index}
                  className="bg-gray-700 p-2 rounded-lg text-center"
                >
                  {r}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
