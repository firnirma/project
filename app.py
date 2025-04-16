from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'secret'  # для сессий

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        session["name"] = name
        session["balance"] = 100
        return redirect(url_for("slot"))
    return render_template("login.html")

@app.route("/slot")
def slot():
    if "name" not in session:
        return redirect(url_for("index"))
    return render_template("slot.html", name=session["name"], balance=session["balance"])

@app.route("/spin", methods=["POST"])
def spin():
    if "name" not in session:
        return redirect(url_for("index"))

    bet = int(request.form["bet"])
    if session["balance"] < bet:
        return "Insufficient funds", 403

    session["balance"] -= bet

    symbols = ['🍒', '🍋', '💎']
    results = [random.choice(symbols) for _ in range(3)]

    if results[0] == results[1] == results[2]:
        session["balance"] += bet * 10
        result = "JACKPOT!"
    else:
        result = "Try again!"

    return render_template("slot.html", name=session["name"], balance=session["balance"], result=result, slots=results)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
