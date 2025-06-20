from flask import Flask, render_template, redirect, url_for
from riddles import riddles

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/level/<int:level>")
def level(level):
    if level >= len(riddles):
        return redirect(url_for('victory'))

    riddle = riddles[level]
    # Pass the riddle question and correct answer (lowercase) to template
    return render_template(
        "level.html",
        riddle=riddle["question"],
        level=level + 1,
        answer=riddle["answer"].lower()
    )

@app.route("/victory")
def victory():
    return render_template("victory.html")

if __name__ == "__main__":
    app.run(debug=True)
