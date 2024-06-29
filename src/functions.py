import re
import src.constants as c
import src.leaderboard as db
import html
from colorama import Fore, Style, init


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
    username = input(Fore.YELLOW+"Hello! To begin, please enter a username> ").strip()
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
    # print("\n")
    print("----------------------------")
    
    for formatted_category in formatted_categories:
        print(formatted_category)
    print("----------------------------")
    # print("\n")
    category = str(input(Fore.YELLOW+"Please select a category by its ID> "))
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
        print(Fore.BLUE+f"  {chr(97 + i)}. {html.unescape(choice)}")

    mapping = {}
    for i, choice in enumerate(arr):
        if choice == ans:
            mapping[chr(i+97)] = "CORRECT"
        else:
            mapping[chr(i+97)] = "INCORRECT"
    return mapping

def print_global_leaderboard():
    # print("Here is the global leaderboard:")

    global_best = db.get_leaderboard()
    users = global_best[0]["scores"]
    max_username_length = max(len(user['username']) for user in users) if users else 0

    # if not global_best:
    #     print("No global best scores available.")

    print("**************************************")
    print("          GLOBAL LEADERBOARD          ")
    print("**************************************")
    for i, entry in enumerate(users):
        print(f"{i+1}.  {entry['username'].ljust(max_username_length)}                  {entry['score']}")
    print("**************************************")
    print("       username saves globally        ")
    print("**************************************")

    print(print_endgame()+" Feel free to play again and try any of our other 23 trivia categories.")

def print_correct_guess():
    return "Correct! +1 point"

def print_incorrect_guess():
    return "Incorrect, sorry!"

def print_endgame(): 
    return "Thank you for playing!"