import requests
import json
import random
import html
import time

# we have (thus far) decided to set question type to default multiple and difficulty to medium
def get_trivia_questions(category, amount=10, difficulty='medium', 
                         question_type='multiple'):
    """
    Gets trivia questions

    This function retrieves trivia questions from the 
    Open Trivia Database API based on the specified parameters.

    Args:
        amount (int): Number of questions to retrieve. Default 10.
        category (int): Category of questions. Corresponds 
            to category ID in database. Defaults None.
        difficulty (str): Difficulty level of questions 
            ('easy', 'medium', 'hard'). Defaults 'medium''.
        question_type (str): Format of questions ('multiple' for 
            multiple-choice, 'boolean' for true/false). Default 'multiple'

    Returns:
        dict: A dictionary containing the response from the API. 
            The dictionary has the following keys:
            - response_code (int): Response code from the API 
                indicating the status of the request.
            - results (list): A list of dictionaries, each representing 
                a trivia question with the following keys:
                - category (str): Category of the question.
                - type (str): Type of the question ('multiple' or 'boolean').
                - difficulty (str): Difficulty level of the question ('easy', 'medium', 'hard').
                - question (str): The trivia question text.
                - correct_answer (str): The correct answer.
                - incorrect_answers (list of str): A list of incorrect answers.
    Raises:
        raises an HTTP request error if there is an error with the API request

    Example:
        call: 
            fetch_trivia_questions(amount=10, category=20, 
            difficulty='hard', question_type=None)

        url construction: 
            url:https://opentdb.com/api.php?amount=10&category=20&difficulty=hard

        output:
            {
            "response_code": 0,
            "results": [
                {
                    "type": "multiple",
                    "difficulty": "hard",
                    "category": "Mythology",
                    "question": "In Greek Mythology, who was the daughter of King Minos?",
                    "correct_answer": "Ariadne",
                    "incorrect_answers": [
                        "Athena",
                        "Ariel",
                        "Alana"
                    ]                                                                                                    
                }, 
                ... 
                (more questions here) 
                ]
            }

    """

    base_url = "https://opentdb.com/api.php"
    params = {
        "amount": amount,
        "category": category,
        "difficulty": difficulty,
        "type": question_type 
    }

    response = requests.get(base_url, params=params)
    while response.status_code == 429:
        print("Our servers are receiving too many requests, please wait a few seconds.")
        time.sleep(5)
        response = requests.get(base_url, params=params)

    response.raise_for_status()
    return response

 
def get_parsed_trivia_questions(category):
    """
    Args:
        category (int): Category of questions. Corresponds to category ID in database

    Returns:
        list of dictionaries representing questions in this format:
        questions = [
            {
                'question': 'What is the capital of France?',
                'choices': ['a) Paris', 'b) London', 'c) Berlin', 'd) Rome'],
                'correct_answer': 'a'
            },
            {
                'question': 'Who wrote "Hamlet"?',
                'choices': ['a) William Shakespeare', 'b) Jane Austen',
                            'c) Charles Dickens', 'd) Mark Twain'],
                'correct_answer': 'a'
            },
        ]
    """
    response = get_trivia_questions(category+8).json()

    questions = []

    # map each q to dict, add lettering to the front of each choice
    for q_data in response["results"]:
        raw_choices = q_data["incorrect_answers"] + [q_data["correct_answer"]]
        random.shuffle(raw_choices)

        lettered_choices = []
        ans_letter, ans_text = None, None

        for letter, choice in zip('abcd', raw_choices):
            disp_text = html.unescape((f'{letter}) {choice}'))
            lettered_choices.append(disp_text)

            if choice == q_data["correct_answer"]:
                ans_letter = letter
                ans_text = disp_text


        

        this_question = {'question': html.unescape(q_data["question"]),
                         'choices': lettered_choices,
                         'correct_answer': ans_text,
                         'correct_answer_letter': ans_letter
                         }
        
        
        questions.append(this_question)
    return questions
    

# parsing this info to look at sample questions
def parse_data(response):
    for data in response['results']:
        # here, we index certain attributes about each of the 10 questions
        print(data['question'])
        print(data['correct_answer'])
        print(data['incorrect_answers'])


if __name__ == "__main__":
    # response = get_trivia_questions(9).json()
    # parse_data(response)
    for i in range(10): 
        print(i)
        get_trivia_questions(10)
