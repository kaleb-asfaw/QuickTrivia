from flask import Flask, render_template, url_for, flash, redirect, request, session
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
import sys,os,git
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.api import get_parsed_trivia_questions
import src.constants as c
from src.loc_scoreboard import update_scoreboard, get_local_scores
from src.leaderboard import add_score, get_leaderboard
import secrets
import sqlite3
from src.constants import ID_TO_CATEGORIES


app = Flask(__name__)
proxied = FlaskBehindProxy(app)

try:
    from config import SECRET_KEY
    app.config['SECRET_KEY'] = SECRET_KEY
except ImportError:
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data.strip()


        
        # Validate username against prohibited list
        if username in c.PROHIBITED:
            form.username.errors.append("This username is prohibited. Please choose another one.")
            return render_template('home.html', form=form)
        
        # Make username lowercase if not in protected list
        if username not in c.PROTECTED:
            username = username.lower()
        

        category = form.category.data
        session['username'] = username
        session['category'] = category
        return redirect(url_for('start'))
    return render_template('home.html', form=form)

@app.route('/start', methods=['GET', 'POST'])
def start():
    username = session.get('username')
    category = session.get('category')
    category_num = int(category)

    # Fetch the questions for the selected category
    questions = get_parsed_trivia_questions(category_num)
    
    # Render the quiz page with the username and questions
    return render_template('gamepage.html', username=username, 
                           questions=questions, category=c.ID_TO_CATEGORIES[category_num])


@app.route("/results", methods=['POST', 'GET'])
def results():
    
    # calculate score if necessary
    if request.method == 'POST':
        username = request.form['username']
        category = request.form['category']
        questions = []
        

        index = 0
        # populate questions from form
        while f'questions[{index}][question]' in request.form:
            question_data = {
                'question': request.form[f'questions[{index}][question]'],
                'correct_answer': request.form[f'questions[{index}][correct_answer]'],
                'choices': request.form.getlist(f'questions[{index}][choices][]')
            }
            questions.append(question_data)
            index += 1

        

        score = 0
        for i, question in enumerate(questions):

            
            # Get selected answer for each question
            selected_answer = request.form.get(f'question{i + 1}')
            if selected_answer is None: # safety for unanswered questions
                continue

            letter_choice = selected_answer[0]
            if letter_choice == question['correct_answer']:
                score += 1

        results_str = f'Your score is {score}/{len(questions)}'

        update_scoreboard(username, score)         # update the sqlite3 database
        local_scores = get_local_scores()          # get the top 10 local scores [username, score]
        add_score(username, score)            # update firebase_admin
        global_best = get_leaderboard()
        global_scores =  global_best[0]["scores"]



    else:
        results_str = f'Play to see your score!'
        local_scores = get_local_scores()
        global_best = get_leaderboard()
        global_scores =  global_best[0]["scores"]


    return render_template('results.html', results_str = results_str, local_scores = local_scores, global_scores = global_scores)
    
@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/quicktrivia/QuickTrivia')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")