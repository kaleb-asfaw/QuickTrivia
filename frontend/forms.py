from flask_wtf import FlaskForm
from wtforms import StringField, SelectField # PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length #, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
            validators=[DataRequired(), Length(min=2, max=12)])
    category = SelectField('Select a trivia category', choices=[
        ('1', 'General Knowledge'),
        ('2', 'Entertainment: Books'),
        ('3', 'Entertainment: Film'),
        ('4', 'Entertainment: Music'),
        ('5', 'Entertainment: Musicals & Theatres'),
        ('6', 'Entertainment: Television'),
        ('7', 'Entertainment: Video Games'),
        ('8', 'Entertainment: Board Games'),
        ('9', 'Science & Nature'),
        ('10', 'Science: Computers'),
        ('11', 'Science: Mathematics'),
        ('12', 'Mythology'),
        ('13', 'Sports'),
        ('14', 'Geography'),
        ('15', 'History'),
        ('16', 'Politics'),
        ('17', 'Art'),
        ('18', 'Celebrities'),
        ('19', 'Animals'),
        ('20', 'Vehicles'),
        ('21', 'Entertainment: Comics'),
        ('22', 'Science: Gadgets'),
        ('23', 'Entertainment: Japanese Anime & Manga'),
        ('24', 'Entertainment: Cartoon & Animations'),
    ], validators=[DataRequired()])
    

    # unused fields
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password',
#                                      validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Sign Up')