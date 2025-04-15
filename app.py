from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"

def check_winner():
    lines = board + list(map(list, zip(*board)))  # строки и столбцы
    lines.append([board[i][i] for i in range(3)])  # диагональ \
    lines.append([board[i][2 - i] for i in range(3)])  # диагональ /
    for line in lines:
        if line.count(line[0]) == 3 and line[0] != "":
            return line[0]
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    global current_player
    data = request.get_json()
    row, col = data["row"], data["col"]
    if board[row][col] == "":
        board[row][col] = current_player
        winner = check_winner()
        response = {"board": board, "winner": winner}
        current_player = "O" if current_player == "X" else "X"
        return jsonify(response)
    return jsonify({"error": "Invalid move"}), 400

if __name__ == "__main__":
    app.run(debug=True)


