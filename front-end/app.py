from flask import Flask, render_template, url_for, flash, redirect, url_for, request
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import SECRET_KEY
from src.api import get_parsed_trivia_questions
import secrets






app = Flask(__name__)                    # this gets the name of the file so Flask knows it's name
proxied = FlaskBehindProxy(app)
# INSTRUCTIONS TO RUN APP: # TODO: figure out if we need secret keys for real???
# 1. open python interpreter by running python3 in terminal
# 2. run import secrets
# 3. run secrets.token_hex(16), then exit() to exit the interpreter
# 4. create a file called config.py (in the quicktrivia folder) and add this line: SECRET_KEY = 'paste your secret key here'
app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route("/")                          # this tells you the URL the method below is related to
def home():
    return render_template('home.html', subtitle='Home', text='This is the home page')   # this prints HTML to the webpage

@app.route("/results", methods=['POST', 'GET'])
def results():

    # calculate score if necessary
    if request.method == 'POST':
        score = 0
        for i, question in enumerate(questions):
            # Get the selected answer for each question
            selected_answer = request.form.get(f'question{i + 1}')
            if selected_answer is None: # safety for unanswered questions
                continue

            letter_choice = selected_answer[0]
            if letter_choice == question['correct_answer']:
                score += 1

        results_str = f'Your score is {score}/{len(questions)}'
    else:
        results_str = f'Play to see your score!'

    return render_template('results.html', results_str = results_str)


category = 1 # TODO: update this to take the input from home.html
questions = get_parsed_trivia_questions(category)

@app.route("/gamepage")
def gamepage():
    return render_template('gamepage.html', questions=questions)



if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0")