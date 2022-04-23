from flask import redirect, render_template, request
from init import app
import users

@app.route("/")
def index():
    logged_in = users.is_logged_in()
    return render_template("index.html", logged_in=logged_in)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", login_failed=True)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_rep = request.form["password_rep"]
        if password_rep != password:
            return render_template("register.html", pws_not_matching=True)
        elif users.register(username, password):
            return redirect("/")
        else:
            return render_template("register.html", username_taken=True)

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "GET":
        return render_template("account.html")
    if request.method == "POST":
        old_password = request.form["old_password"]
        password = request.form["password"]
        password_rep = request.form["password_rep"]
        if password_rep != password:
            return render_template("account.html", pws_not_matching=True)
        elif users.update_password(old_password, password):
            return redirect("/account")
        else:
            return render_template("account.html", incorrect_pw=True)

@app.route("/lobbies")
def lobbies():
    return "Game lobby creation/join page. Not yet implemented."

#The game/lobby pages will be entered by clicking a button in /lobbies 
#(or by clicking a join link if I implement that)
@app.route("/game/<int:lobby_id>")
def game(lobby_id: int):
    return "Page for playing the game. This will be written in Nim. The clients will communicate to the server via a Websocket url that is specific to the game lobby. Not yet implemented."

@app.route("/lobby/<int:lobby_id>")
def lobby(lobby_id: int):
    return "Page for editing lobby settings and the lobby owner can start the game from here. This will be written in Nim. The clients will communicate to the server via a Websocket url that is specific to the game lobby. Not yet implemented."

@app.route("/stats")
def stats():
    return "Page for showing the user's game history/stats. Not yet implemented."
