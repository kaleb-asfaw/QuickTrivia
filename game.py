from api import get_trivia_questions as api
import constants as c
import messages as m
import random

username = str(input("Hello! To begin, please enter a username: "))

print(m.print_categories(c.CATEGORIES))
category = input("Choose the category you'd like to play: ")
while category not in c.NUMS:
    category = input("Please choose a valid category. See the options above and select a corresponding number (1-24): ")

# Here is the trivia match data that should be relayed to users one question at a time
response = api.get_trivia_questions(int(category)+8)


# Now, we process the response
for i, q_data in enumerate(response.json()["results"]):
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
    else:
        m.print_incorrect_guess()

m.print_endgame(category)