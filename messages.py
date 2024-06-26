import html

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
        print(f"   {chr(97 + i)}. {html.unescape(choice)}")

    mapping = {}
    for i, choice in enumerate(arr):
        if choice == ans:
            mapping[chr(i+97)] = "CORRECT"
        else:
            mapping[chr(i+97)] = "INCORRECT"
    return mapping

def print_correct_guess():
    return "Correct! +1 point"

def print_incorrect_guess():
    return "Incorrect, sorry!"

def print_endgame(): # maybe add leaderboards per category
    return "Thanks for playing!"