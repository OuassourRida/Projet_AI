from flask import Flask, request, jsonify
from flask_cors import CORS
from app.models.knn_recommender import recommend

app = Flask(__name__)
CORS(app)


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


@app.route('/recommendations', methods=['POST'])
def recommendations():
    payload = request.get_json(force=True, silent=True) or {}
    hotels = payload.get('hotels') or []
    try:
        top_k = int(payload.get('top_k', 10))
    except Exception:
        top_k = 10
    try:
        recs = recommend(hotels, top_k=top_k)
        return jsonify({'recommendations': recs})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500


if __name__ == '__main__':
    # For local development only
    app.run(host='0.0.0.0', port=5000, debug=True)
