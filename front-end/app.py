from flask import Flask, render_template, url_for, flash, redirect, url_for, request
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import SECRET_KEY


questions = [
    {
        'question': 'What is the capital of France?',
        'choices': ['a) Paris', 'b) London', 'c) Berlin', 'd) Rome'],
        'correct_answer': 'a'
    },
    {
        'question': 'Who wrote "Hamlet"?',
        'choices': ['a) William Shakespeare', 'b) Jane Austen', 'c) Charles Dickens', 'd) Mark Twain'],
        'correct_answer': 'a'
    },
    # Add more questions here as needed
]


app = Flask(__name__)                    # this gets the name of the file so Flask knows it's name
proxied = FlaskBehindProxy(app)
# INSTRUCTIONS TO RUN APP:
# 1. open python interpreter by running python3 in terminal
# 2. run import secrets
# 3. run secrets.token_hex(16), then exit() to exit the interpreter
# 4. create a file called config.py and add this line: SECRET_KEY = 'paste your secret key here'
app.config['SECRET_KEY'] = SECRET_KEY

@app.route("/")                          # this tells you the URL the method below is related to
def home():
    return render_template('home.html', subtitle='Home', text='This is the home page')   # this prints HTML to the webpage

@app.route("/results")
def second_page():
    return render_template('results.html', subtitle='Results Page', text='This is the results page')

@app.route("/gamepage")
def gamepage():
    return render_template('gamepage.html', questions=questions)

# TODO: merge this page with results so that we display the users' individual score and then the leaderboard stuffs
@app.route('/submit-trivia', methods=['POST'])
def submit_trivia():
    score = 0
    for i, question in enumerate(questions):
        # Get the selected answer for each question
        selected_answer = request.form.get(f'question{i + 1}')[0]
        # Check if the selected answer is correct
        # print('selected answer: ', selected_answer)
        # print('correct answer', question['correct_answer'])
        if selected_answer == question['correct_answer']:
            score += 1
    return f'Your score is {score}/{len(questions)}'

# DELETE BELOW LATER (kept for reference to figure out username submission things)

# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit(): # checks if entries are valid
#         flash(f'Account created for {form.username.data}!', 'success')
#         return redirect(url_for('home')) # if so - send to home page
#     return render_template('register.html', title='Game', form=form)

if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0")