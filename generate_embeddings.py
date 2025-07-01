from sentence_transformers import SentenceTransformer
import firebase_admin
from firebase_admin import credentials, firestore

# 🔌 Firebase setup
if not firebase_admin._apps:
    cred = credentials.Certificate(
        "thewill-c232a-firebase-adminsdk-kcl17-e81cd4e648.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding_for_user(user_data):
    # Extract necessary fields
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
