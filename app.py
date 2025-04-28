from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        session["name"] = name
        session["balance"] = 500
        return redirect(url_for("slot"))
    return render_template("login.html")

@app.route("/slot", methods=["GET", "POST"])
def slot():
    if "name" not in session:
        return redirect(url_for("index"))
    
    result = None
    slots = ['❓', '❓', '❓']

    if request.method == "POST":
        bet = int(request.form["bet"])

        if session["balance"] >= bet:
            session["balance"] -= bet

            symbols = ['🍒', '🍋', '💎', '🔔', '⭐']
            slots = [random.choice(symbols) for _ in range(3)]

            if slots[0] == slots[1] == slots[2]:
                win_amount = bet * 10
                session["balance"] += win_amount
                result = f"🎉 JACKPOT! You win {win_amount} coins!"
            else:
                result = "Try again!"

        else:
            result = "Not enough balance!"

    return render_template("slot.html", name=session["name"], balance=session["balance"], result=result, slots=slots)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
