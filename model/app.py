from flask import Flask, request, jsonify
from flask_cors import CORS
from model import get_recommendations

app = Flask(__name__)
CORS(app)  # allows frontend (React) to communicate

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    movie_name = data.get('movie')
    if not movie_name:
        return jsonify({'error': 'Movie name required'}), 400
    
    result = get_recommendations(movie_name)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
