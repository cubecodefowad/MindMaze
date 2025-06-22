from flask import Flask, render_template, redirect, url_for, session, request
import os
import random
import time
from riddles import riddles

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    session.clear()
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_game():
    session['username'] = request.form.get('username', 'Player')
    session['start_time'] = time.time()
    session['score'] = 0
    session['lives'] = 3
    return redirect(url_for('level_view', level=1))

@app.route("/level/<int:level>")
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
        username=session.get('username', 'Player'),
        start_time=session.get('start_time')
    )

@app.route("/submit_answer/<int:level>", methods=["POST"])
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
def victory():
    score = session.get('score', 0)
    session.clear()
    return render_template("victory.html", score=score)

@app.route("/game-over")
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

if __name__ == "__main__":
    app.run(debug=True)



