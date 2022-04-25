from flask import redirect, render_template, request, url_for
from init import app
import json
import users, game_stats, lobbies

@app.route("/")
def index():
    logged_in = users.is_logged_in()
    return render_template("index.html", logged_in=logged_in, 
                           games_played=game_stats.games_played(), active_games=lobbies.active_games())

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
        #TODO: render_template SHOULD NOT BE CALLED IN POST because then refreshing after form submit will try to resubmit it
        #Maybe use the pattern used in post action send_friend_req of /friends page
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
    if users.is_logged_in():
        if request.method == "GET":
            return render_template("account.html", username=users.username(), stats_vis=users.stats_vis()) 
        if request.method == "POST": 
            #TODO: render_template SHOULD NOT BE CALLED IN POST because then refreshing after form submit will try to resubmit it
            #Maybe use the pattern used in post action send_friend_req of /friends page
            if request.form["action"] == "password_change":
                old_password = request.form["old_password"]
                password = request.form["password"]
                password_rep = request.form["password_rep"]
                if password_rep != password:
                    return render_template("account.html", username=users.username(), stats_vis=users.stats_vis(), pws_not_matching=True)
                elif users.update_password(old_password, password):
                    return render_template("account.html", username=users.username(), stats_vis=users.stats_vis(), pw_update_success=True)
                else:
                    return render_template("account.html", username=users.username(), stats_vis=users.stats_vis(), incorrect_pw=True)
            elif request.form["action"] == "set_stats_vis":
                if users.set_stats_vis(request.form["stats_vis"]):
                    return render_template("account.html", username=users.username(), stats_vis=users.stats_vis())
    else:
        return "Can't access user account settings while not logged in. This page will have a button to go back to the front page when I make it."

@app.route("/lobbies")
def play():
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
    if users.is_logged_in():
        return render_template(
            "stats.html", 
            username=users.username(), 
            game_history=game_stats.user_n_last_games(20),
            games_played=game_stats.user_games_played()
        )
    else:
        return "Can't access user stats while not logged in. This page will have a button to go back to the front page when I make it."

@app.route("/friends", methods=["GET", "POST"])
def friends():
    if users.is_logged_in():
        if request.method == "GET":
            return render_template(
                "friends.html", 
                friends=users.friends_of_user(),
                friend_reqs_in=users.friend_reqs_to_user(),
                friend_reqs_out=users.friend_reqs_from_user()
            )
        if request.method == "POST":
            #It's safe to parse id as an int, because it comes from a hidden field of the form, that the user cannot modify in normal use
            if request.form["action"] == "accept_friend_req":
                users.accept_friend_req(int(request.form["id"])) 
            elif request.form["action"] == "remove_friend":
                users.remove_friend(int(request.form["id"]))
            elif request.form["action"] == "send_friend_req":
                result = users.send_friend_req(request.form["username"])
                if not result.success:
                    return redirect(url_for('.error', msg=result.result_or_msg))
            return redirect("/friends")
    else:
        return "Can't access friends list while not logged in. This page will have a button to go back to the front page when I make it."

@app.route("/error")
def error():
    msg = request.args['msg']
    return render_template("error.html", error_msg=msg)
