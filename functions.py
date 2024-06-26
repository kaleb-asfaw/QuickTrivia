import re
import constants as c
import leaderboard as db

def validate_username(username):
    # Convert username to lowercase
    if username not in c.PROTECTED:
        username = username.lower()
    else:
        return "VALID"

    if username in c.PROHIBITED:
        return "INVALID: BANNED NAME"

    # Check if the username starts with a space or is empty
    if username.startswith(' ') or len(username) == 0:
        return "INVALID: SPACE"

    # Check if the username contains more than one consecutive space
    if '  ' in username:
        return "INVALID: DOUBLE SPACE"

    # Check if the username exceeds the character limit
    if len(username) > 12:
        return "INVALID: LONG"

    return "VALID"

def get_username():
    username = input("Hello! To begin, please enter a username> ").strip()
    while True:
        msg = validate_username(username)
        if username in c.PROTECTED:
            return username

        elif msg == "VALID":
            return username.lower()

        elif msg == "INVALID: BANNED NAME":
            print("\n")
            username = input("Your username is banned, please try a different username> ").strip()
    
        elif msg == "INVALID: SPACE":
            print("\n")
            username = input("Your username has a space at the beginning or is empty, please try a different username> ").strip()

        elif msg == "INVALID: DOUBLE SPACE":
            print("\n")
            username = input("Your username contains a double space, please try a different username> ").strip()
            
        elif msg == "INVALID: LONG":
            print("\n")
            username = input("Your username is longer than 12 characters, please try a different username> ").strip()
            
        else:
            raise ValueError("get_username(function) isn't catching error")
        
        
def print_categories(categories):
    '''
    Given list of tuples (category name, ID) will display info to users.
    '''
    formatted_categories = []
    for category in categories:
        name, id = category
        formatted_categories.append(f"- {name} (ID: {id})")
    

    print("Here is the list of trivia categories:")
    print("\n")
    print("----------------------------")
    
    for formatted_category in formatted_categories:
        print(formatted_category)
    print("----------------------------")
    # print("\n")
    category = str(input("Please select a category by its ID> "))
    return category

def print_options(arr, ans):
    '''
    Given an array of 4 options, prints to user and returns
    a dictionary mapping choice in letter to whether the
    answer was correct or not.
    '''
    if len(arr) != 4:
        raise ValueError("There must be exactly 4 options.")

    # Print each option with its corresponding letter
    for i, choice in enumerate(arr):
        print(f"{chr(97 + i)}. {choice}")

    mapping = {}
    for i, choice in enumerate(arr):
        if choice == ans:
            mapping[chr(i+97)] = "CORRECT"
        else:
            mapping[chr(i+97)] = "INCORRECT"
    return mapping

def print_global_leaderboard():
    print(f"Thank you for playing, feel free to play again and try any of our other 23 trivia categories!")
    print("Here is the global leaderboard:")

    global_best = db.get_leaderboard()
    if global_best:
        for i, entry in enumerate(global_best[0]["scores"]):
            print(f"{i + 1}. {entry['username']} - {entry['score']} points")
    else:
        print("No global best scores available.")

def print_correct_guess():
    print("Good job I guess.")

def print_incorrect_guess():
    print("Ha, loser!")

def print_endgame(): # maybe add leaderboards per category
    print("Thank you for playing!")