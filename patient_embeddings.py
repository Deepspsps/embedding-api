from sentence_transformers import SentenceTransformer
import firebase_admin
from firebase_admin import credentials, firestore

# 🔌 Firebase setup
cred = credentials.Certificate(
    "thewill-c232a-firebase-adminsdk-kcl17-e81cd4e648.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

# 🔁 Loop through patients
users_ref = db.collection("users")
docs = users_ref.stream()

for doc in docs:
    data = doc.to_dict()
    if data.get("role") != "patient":
        continue

    name = data.get("name", "")
    category = data.get("category", "")
    health = data.get("healthHistory", "")
    hours = data.get("assistanceHours", "")
    address = data.get("address", "")

    input_string = f"Patient named {name} needs help with {category}. Health history includes: {health}. Requires assistance for {hours} hours. Located at {address}."

    try:
        embedding = model.encode(input_string).tolist()
        users_ref.document(doc.id).update({"embedding": embedding})
        print(f"✅ Embedded: {name}")
    except Exception as e:
        print(f"❌ Failed for {name}: {e}")
