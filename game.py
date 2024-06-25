from api import get_trivia_questions
import constants as c
import messages as m
import loc_scoreboard as sb
import random

# We will store the username in a local database as well as the total points scored
# If the username is already in the database the total score will be updated
username = str(input("Hello! To begin, please enter a username> "))
points = 0; # points scored in this game session
num_questions = 0

category = m.print_categories(c.CATEGORIES)
while category not in c.NUMS:
    category = input("Please choose a valid category. See the options above and select a corresponding number (1-24): ")

# Here is the trivia match data that should be relayed to users one question at a time
response = get_trivia_questions(int(category)+8)


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

    num_questions += 1
    if mapping[choice] == "CORRECT":
        m.print_correct_guess()
        points += 1
        print("You got one point! Current points: ", points)
    else:
        m.print_incorrect_guess()
        print("No point for you :( current points: ", points)

# update the scoreboard
sb.update_scoreboard(username, points)

#print ending message and current leaderboard
print()
print(f"Congratulations, you got {points} / {num_questions} questions!")

sb.print_scoreboard()
m.print_endgame(category)