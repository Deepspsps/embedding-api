import firebase_admin
from firebase_admin import credentials, firestore

# Step 1: connect to Firestore
cred = credentials.Certificate(
    "thewill-c232a-firebase-adminsdk-kcl17-e81cd4e648.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# reference the users collection
users_ref = db.collection("users")
docs = users_ref.stream()

# loop through all users and filter patients only
for doc in docs:
    data = doc.to_dict()

    if data.get("role") == "patient":
        health = data.get("healthHistory", "")
        category = data.get("category", "")
        hours = data.get("assistanceHours", "")
        address = data.get("address", "")
        name = data.get("name", "")

        embedding_input = f"Patient named {name} needs help with {category}. Health history includes: {health}. Requires assistance for {hours} hours. Located at {address}."

        print("Embedding input:\n", embedding_input)
        print("------")
