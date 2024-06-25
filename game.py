import firebase_admin
from firebase_admin import credentials, firestore
import leaderboard as db
from api import get_trivia_questions
import constants as c
import messages as m
import random

username = str(input("Hello! To begin, please enter a username: "))

category = m.print_categories(c.CATEGORIES)
while category not in c.NUMS:
    category = input("Please choose a valid category. See the options above and select a corresponding number (1-24): ")

# Here is the trivia match data that should be relayed to users one question at a time
response = get_trivia_questions(int(category)+8)


score = 0
# Now, we process the response
for i, q_data in enumerate(response["results"]):
    question = q_data["question"]
    ans = q_data["correct_answer"]
    options = q_data["incorrect_answers"] + [ans]
    random.shuffle(options)

    print(f"Question {i+1}: {question}")
    mapping = m.print_options(options, ans)
    choice = input("Enter your answer (a, b, c, or d): ")
    while choice not in ["a", "b", "c", "d"]:
        choice = input("Invalid selection, please enter one of the following: a, b, c, or d: ")

    if mapping[choice] == "CORRECT":
        m.print_correct_guess()
        score += 5
    else:
        m.print_incorrect_guess()
        score -= 2
m.print_endgame()

# now, let's update the global leaderboard
db.add_score(username, score)