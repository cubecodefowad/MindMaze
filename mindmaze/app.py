from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/level/1")
def level1():
    return render_template("level1.html")

@app.route("/victory")
def victory():
    return render_template("victory.html")

if __name__ == "__name__":
    app.run(debug=True)