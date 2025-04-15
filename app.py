from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/yes")
def yes():
    return redirect(url_for("slot"))

@app.route("/no")
def no():
    return render_template("denied.html")

@app.route("/slot")
def slot():
    return render_template("slot.html")  # временно заглушка

if __name__ == "__main__":
    app.run(debug=True)
