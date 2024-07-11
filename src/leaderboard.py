import firebase_admin
from firebase_admin import credentials, firestore
import os
import base64
import json

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Check if credentials.json exists
cred_path = sys.path[0] + "/credentials.json"

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# # encoded the credentials in a base64 string as an env variable
# credentials_base64 = os.getenv('CREDENTIALS_JSON_BASE64')
# credentials_json = None

# if credentials_base64:
#     try:
#         credentials_json = base64.b64decode(credentials_base64).decode('utf-8')
#         credentials_data = json.loads(credentials_json)
#         with open('temp_credentials.json', 'w') as f:
#             f.write(credentials_json)
#         cred = credentials.Certificate('temp_credentials.json')
#         firebase_admin.initialize_app(cred)
#         print("PROPERLY USED ENV VAR")
#         os.remove('temp_credentials.json')
#     except Exception as e:
#         raise EnvironmentError("Failed to decode or parse credentials from the environment variable. Error: {}".format(str(e)))
# else:
#     print("NOT USING ENV VAR")
#     cred_path = "credentials.json"
#     if not os.path.exists(cred_path):
#         raise ValueError("The credentials are not set and the credentials.json file is missing.")

#     cred = credentials.Certificate(cred_path)
#     firebase_admin.initialize_app(cred)


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