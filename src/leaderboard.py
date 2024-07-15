import firebase_admin
from firebase_admin import credentials, firestore
import os
import base64
import json

# configures the connection of game --> firebase DB by
# 1) encoding JSON file with credentials into a 64-bit string 
#    and storing as env variable (in GitHub workflow as well)
# 2) decoding it when file is called 
# 3) initializing Firebase connection (boilerplate code)

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
    '''
    Given username and final score, add the score to the noSQL schema.

    Stucture:
    {
        user1: [score1, score2, ......],
        user2: [score1, .....],
        ...
        ...
        ...
        userN: [score1, .....],
        global_best: [1st_highest, 2nd_highest, 3rd_highest],

    }
        
    '''
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
    '''
    Given a score and username, we update the leaderboard to display the 
    [new] top scores in the database.

    '''
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