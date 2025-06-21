from flask import Flask, render_template, redirect, url_for
from riddles import riddles

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/level/<int:level>")
def level_view(level):
    # level starts from 1
    if level > len(riddles):
        return redirect(url_for("victory"))

    riddle_data = riddles[level - 1]  # zero-indexed list
    return render_template(
        "level.html",
        riddle=riddle_data["question"],
        answer=riddle_data["answer"].lower(),
        level=level
    )

@app.route("/victory")
def victory():
    return render_template("victory.html")

if __name__ == "__main__":
    app.run(debug=True)
