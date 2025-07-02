import os
from flask import Flask, request, jsonify
from generate_embeddings import generate_embedding_for_user

print("🚀 Starting Flask setup...")  # New line

app = Flask(__name__)
SECRET_TOKEN = os.environ.get("EMBED_API_SECRET")


@app.route('/generate-embedding', methods=['POST'])
def generate():
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Bearer {SECRET_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

    user_data = request.get_json()
    if not user_data:
        return jsonify({"error": "No user data received"}), 400

    try:
        generate_embedding_for_user(user_data)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("🌐 Preparing to run Flask...")  # New line
    port = int(os.environ.get("PORT", 5000))
    print(f"✅ Running on port: {port}")  # New line
    app.run(host="0.0.0.0", port=port)
