import leaderboard as db
from api import get_trivia_questions
import constants as c
import functions as f
import loc_scoreboard as sb
import random
import html
from colorama import Fore, Style, init

init()  # Initialize colorama

# We will store the username in a local database as well as the total points scored
# If the username is already in the database the total score will be updated
username = f.get_username()
print(Fore.GREEN+f'Hi {username}')
points = 0    # points scored in this game session
num_questions = 0

category = f.print_categories(c.CATEGORIES)
while category not in c.NUMS:
    category = input(Fore.RED+"Please choose a valid category. See the options above and select a corresponding number (1-24): ")

# Here is the trivia match data that should be relayed to users one question at a time
response = get_trivia_questions(int(category)+8).json()

print(Fore.MAGENTA + "Trivia starts now!")

# Now, we process the response
for i, q_data in enumerate(response["results"]):
    question = html.unescape(q_data["question"])    # we html unescape to remove weird & : thingies
    ans = q_data["correct_answer"]
    options = q_data["incorrect_answers"] + [ans]
    random.shuffle(options)
    print(Fore.BLUE+'>>>')
    print(f"Question {i+1}: {question}")
    mapping = f.print_options(options, ans)
    choice = input(Fore.YELLOW+"Enter your answer (a, b, c, or d): ")
    while choice.lower() not in ["a", "b", "c", "d"]:
        choice = input("Invalid selection, please enter one of the following: a, b, c, or d: ")

    num_questions += 1
    if mapping[choice.lower()] == "CORRECT":
        print(Fore.GREEN+f.print_correct_guess())
        points += 1
        print(Fore.MAGENTA + "Current points: ", points)
    else:
        print(Fore.RED+f.print_incorrect_guess())
        print(Fore.MAGENTA + "Current points: ", points)
# update the scoreboard
sb.update_scoreboard(username, points)
# now, let's update the global leaderboard
db.add_score(username, points)

# print ending message and current leaderboard
print(Fore.MAGENTA+"~~~")
print(Fore.MAGENTA+"That's the end of the Trivia")
print(Fore.GREEN + f"you got {points} / {num_questions} questions!") 
sb.print_scoreboard()
f.print_global_leaderboard()