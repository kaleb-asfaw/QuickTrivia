import firebase_admin
from firebase_admin import credentials, firestore
import os
import base64
import json


credentials_base64 = os.getenv('CREDENTIALS_JSON_BASE64')
if not credentials_base64:
    raise EnvironmentError("Environment variable for Firebase was not set")

credentials_json = None
credentials_json = base64.b64decode(credentials_base64).decode('utf-8')
credentials_data = json.loads(credentials_json)
with open('temp_credentials.json', 'w') as f:
    f.write(credentials_json)
cred = credentials.Certificate('temp_credentials.json')
firebase_admin.initialize_app(cred)
os.remove('temp_credentials.json')
    

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