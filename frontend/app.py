from flask import Flask, render_template, url_for, flash, redirect, request, session, jsonify
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
import sys,os,git
import secrets
import sqlite3
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.api import get_parsed_trivia_questions
import src.constants as c
from src.loc_scoreboard import update_scoreboard, get_local_scores
from src.leaderboard import add_score, get_leaderboard
from src.constants import ID_TO_CATEGORIES
from src.hostAI import get_commentary


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
    username_prepopulate = request.args.get('username', None)  # Retrieves the username if provided

    if username_prepopulate:
        form.username.data = username_prepopulate  # Prepopulates the form with the username

    if form.validate_on_submit():
        username = form.username.data.strip()
        if username in c.PROHIBITED:
            form.username.errors.append("This username is prohibited. Please choose another one.")
            return render_template('home.html', form=form)

        if username not in c.PROTECTED:
            username = username.lower()

        category = form.category.data
        session['username'] = username
        session['category'] = category

        return redirect(url_for('start'))


    return render_template('home.html', form=form)



@app.route('/start', methods = ['GET'])
def start():
    username = session.get('username')
    category = session.get('category')
    category_num = int(category)
    session['category_disp'] = c.ID_TO_CATEGORIES[category_num]
    

    questions = get_parsed_trivia_questions(category_num)

    
    session['current_question'] = 0
    session['score'] = 0
    session['streak'] = 0
    session['questions'] = questions

    return redirect(url_for('game'))

    return render_template('gamepage.html', username=username, 
                           questions=questions, category=c.ID_TO_CATEGORIES[category_num])


@app.route('/increment-question', methods=['GET'])
def increment_question():
    if session['current_question'] < 9: # can still increment
        print('HELLO, INCREMENTING YOUR QUESTION')
        session['current_question'] += 1
        return redirect(url_for('game'))
    else:
        print('HELLO, YOU ARE DONE WITH THE TRIVIA')
        return redirect(url_for('results', from_increment_question=True))



@app.route('/game', methods=['GET', 'POST'])
def game():
    
    username = session.get('username')
    curr_question = session.get('questions')[session.get('current_question')]
    category = session['category_disp']
    
    
    # Render the quiz page with the username and questions
    return render_template('gamepage.html', username=username, 
                           question=curr_question, category=category)

@app.route('/feedback', methods=['POST'])
def feedback():
    print(f'I AM TAKING YOU TO THE FEED BACK PAGE AND YOUR CURRENT QUESTION IS {session['current_question']}')
    if session['current_question'] < 10:

        username = session.get('username')
        category = session.get('category')
        category_num = int(category)
        session['category_disp'] = c.ID_TO_CATEGORIES[category_num]
        questions = session.get('questions')
        curr_question = questions[session['current_question']]
        streak_before = session['streak']

        if request.method == 'POST': # got here from feedback (not from start)
            index = session['current_question']
            user_answer = request.form.get(f'answer')
            session['user_answer'] = user_answer
            correct_answer = questions[index]['correct_answer']

            is_correct = user_answer and user_answer[0] == correct_answer
            if is_correct:
                session['score'] += 1
                session['streak'] += 1
            else:
                session['streak'] = 0
            
        feedback = get_commentary(curr_question, user_answer, is_correct, (streak_before, session['streak']))

        session['feedback'] = feedback
        
        return render_template('feedback.html', feedback=session['feedback'], username = session['username'], category = session['category_disp'], question = session.get('questions')[session.get('current_question')])
    else:
        return redirect(url_for('results'))

@app.route("/results", methods=['POST', 'GET'])
def results():
    print('YOU ARRIVED TO THE RESULTS PAGE')
    finished_trivia = request.args.get('from_increment_question', False)

    # calculate score if necessary
    if finished_trivia:
        username = session.get('username')
        questions = session.get('questions')
        score = session.get('score')
        streak = session.get('streak')


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