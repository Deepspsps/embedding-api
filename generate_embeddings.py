from sentence_transformers import SentenceTransformer
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

model = SentenceTransformer("sentence-transformers/paraphrase-albert-small-v2")


def generate_embedding_for_user(user_data):
    # 🔌 Initialize Firebase inside the function
    if not firebase_admin._apps:
        firebase_json = os.environ.get("FIREBASE_CREDENTIALS")
        if not firebase_json:
            raise ValueError("FIREBASE_CREDENTIALS env var is missing!")

        firebase_dict = json.loads(firebase_json)
        cred = credentials.Certificate(firebase_dict)
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    uid = user_data.get("uid")
    if not uid:
        raise ValueError("Missing UID")

    qual = user_data.get("qualifications", "")
    exp = user_data.get("experienceYears", "")
    work = user_data.get("workHistory", "")
    availability = user_data.get("availability", "")
    location = user_data.get("location", "")
    reason = user_data.get("reasonForApplying", "")

    input_string = f"{qual} with {exp} years of experience. Previously worked in: {work}. Available for {availability} hours. Based in {location}. Motivation: {reason}"

    try:
        embedding = model.encode(input_string).tolist()
        db.collection("users").document(uid).update({"embedding": embedding})
        print(f"✅ Embedded: {user_data.get('name')}")
    except Exception as e:
        print(f"❌ Failed for {user_data.get('name')}: {e}")
        raise e
