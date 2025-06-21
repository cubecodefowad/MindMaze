from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
import os
import random
import time
from riddles import riddles

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/start", methods=["POST"])
@login_required
def start_game():
    session['start_time'] = time.time()
    session['score'] = 0
    session['lives'] = 3
    return redirect(url_for('level_view', level=1))

@app.route("/level/<int:level>")
@login_required
def level_view(level):
    if session.get('lives', 0) <= 0:
        return redirect(url_for("game_over"))

    if level > len(riddles):
        return redirect(url_for("victory"))

    riddle_data = riddles[level - 1]
    return render_template(
        "level.html",
        riddle=riddle_data["question"],
        hint=riddle_data["hint"],
        level=level,
        score=session.get('score', 0),
        lives=session.get('lives', 3),
        username=current_user.username,
        start_time=session.get('start_time')
    )

@app.route("/submit_answer/<int:level>", methods=["POST"])
@login_required
def submit_answer(level):
    user_answer = request.form.get("answer", "").lower().strip()
    correct_answer = riddles[level - 1]["answer"].lower()

    if user_answer == correct_answer:
        session['score'] = session.get('score', 0) + 1
        return redirect(url_for("level_view", level=level + 1))
    else:
        session['lives'] = session.get('lives', 3) - 1
        if session['lives'] > 0:
            return redirect(url_for("level_view", level=level))
        else:
            return redirect(url_for("game_over"))

@app.route("/victory")
@login_required
def victory():
    score = session.get('score', 0)
    session.clear()
    return render_template("victory.html", score=score)

@app.route("/game-over")
@login_required
def game_over():
    score = session.get('score', 0)
    session.clear()
    failure_messages = [
        "The maze has claimed another mind.",
        "You were so close, yet so far.",
        "Better luck next time, maze runner.",
        "Your journey ends here.",
        "The riddles were too much for you."
    ]
    message = random.choice(failure_messages)
    return render_template("gameover.html", score=score, message=message)

@app.cli.command("create-db")
def create_db():
    """Creates the database."""
    with app.app_context():
        db.create_all()
    print("Database created!")

if __name__ == "__main__":
    app.run(debug=True)



