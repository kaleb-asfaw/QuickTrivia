import firebase_admin
from firebase_admin import credentials, firestore
import sys, os


# Use the environment variable for the path to the service account key
# cred_path = "credentials.json"
cred_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'credentials.json'))
if not cred_path:
    raise ValueError("The credentials are not set.")

# Initialize Firebase Admin SDK with the service account key
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()


def add_score(username, score):
    user_ref = db.collection('leaderboard').document(username)
    user_doc = user_ref.get()

    if user_doc.exists:
        user_scores = user_doc.to_dict().get('scores', [])
        user_scores.append(score)
    else:
        user_scores = [score]

    user_ref.set({'scores': user_scores})

    update_global_best(score, username)

def update_global_best(score, username):
    global_best_ref = db.collection('leaderboard').document('global_best')
    global_best_doc = global_best_ref.get()

    if global_best_doc.exists:
        global_best_scores = global_best_doc.to_dict().get('scores', [])
        global_best_scores.append({'score': score, 'username': username})
        global_best_scores = sorted(global_best_scores, key=lambda x: x['score'], reverse=True)[:10]
    else:
        global_best_scores = [{'score': score, 'username': username}]

    global_best_ref.set({'scores': global_best_scores})


def get_leaderboard():
    leaderboard_ref = db.collection('leaderboard')
    return [doc.to_dict() for doc in leaderboard_ref.order_by('scores', direction=firestore.Query.DESCENDING).stream()]