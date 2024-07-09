from flask import Flask, render_template, url_for, flash, redirect, url_for
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy



app = Flask(__name__)                    # this gets the name of the file so Flask knows it's name
proxied = FlaskBehindProxy(app)
# INSTRUCTIONS TO RUN APP:
# 1. open python interpreter by running python3 in terminal
# 2. run import secrets
# 3. run secrets.token_hex(16), then exit() to exit the interpreter
# 4. uncomment the line below and replace YOUR_SECRET with the output in the terminal
# app.config['SECRET_KEY'] = 'YOUR_SECRET'

@app.route("/")                          # this tells you the URL the method below is related to
def home():
    return render_template('home.html', subtitle='Home', text='This is the home page')   # this prints HTML to the webpage

@app.route("/results")
def second_page():
    return render_template('results.html', subtitle='Results Page', text='This is the results page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0")