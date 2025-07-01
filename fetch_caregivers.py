import firebase_admin
from firebase_admin import credentials, firestore

# Step 1: connect to Firestore
# replace with actual file name
cred = credentials.Certificate(
    "thewill-c232a-firebase-adminsdk-kcl17-e81cd4e648.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# reference the users collection
users_ref = db.collection("users")
docs = users_ref.stream()

# loop through all users and filter caregivers only
for doc in docs:
    data = doc.to_dict()

    if data.get("role") == "caregiver":
        qual = data.get("qualifications", "")
        exp = data.get("experienceYears", "")
        work = data.get("workHistory", "")
        availability = data.get("availability", "")
        location = data.get("location", "")
        reason = data.get("reasonForApplying", "")

        embedding_input = f"{qual} with {exp} years of experience. Previously worked in: {work}. Available for {availability} hours. Based in {location}. Motivation: {reason}"

        print("Embedding input:\n", embedding_input)
        print("------")
