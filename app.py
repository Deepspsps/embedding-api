from flask import Flask, request, jsonify
from generate_embeddings import generate_embedding_for_user

app = Flask(__name__)


@app.route('/generate-embedding', methods=['POST'])
def generate():
    user_data = request.get_json()
    if not user_data:
        return jsonify({"error": "No user data received"}), 400

    try:
        generate_embedding_for_user(user_data)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
