from flask import redirect, render_template, request, url_for
from werkzeug.wrappers.response import Response
from init import app
import users, game_stats, lobbies

def redirect_to_needs_login() -> Response:
    return redirect(url_for('.error', msg="Can't access user stats while not logged in."))

@app.route("/")
def index():
    logged_in = users.is_logged_in()
    return render_template("index.html", logged_in=logged_in, 
                           games_played=game_stats.games_played(), active_games=lobbies.active_games())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        err_name=request.args.get("err_name", "")
        return render_template("login.html", err_name=err_name)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        redirect_to = url_for(".index")
        if not users.login(username, password):
            redirect_to = url_for(".login", err_name="wrong_credentials")
        return redirect(redirect_to)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        err_name=request.args.get("err_name", "")
        return render_template("register.html", err_name=err_name)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_rep = request.form["password_rep"]
        redirect_to = url_for(".index")
        if password_rep != password:
            redirect_to = url_for(".register", err_name="pws_not_matching")
        elif len(username) < 2:
            redirect_to = url_for(".register", err_name="short_username")
        elif len(password) < 6:
            redirect_to = url_for(".register", err_name="short_pw")
        elif not users.register(username, password):
            redirect_to = url_for(".register", err_name="username_taken")
        return redirect(redirect_to)

@app.route("/account", methods=["GET", "POST"])
def account():
    if users.is_logged_in():
        if request.method == "GET":
            return render_template("account.html", username=users.username(), stats_vis=users.stats_vis()) 
        if request.method == "POST": 
            redirect_to = url_for(".account") # Show account page again if there were no errors
            if request.form["action"] == "password_change":
                old_password = request.form["old_password"]
                password = request.form["password"]
                password_rep = request.form["password_rep"]
                if password_rep != password:
                    redirect_to = url_for(".account", err_name="pws_not_matching")
                elif users.update_password(old_password, password):
                    redirect_to = url_for(".account", err_name="pw_updated")
                else:
                    redirect_to = url_for(".account", err_name="wrong_pw")
            elif request.form["action"] == "set_stats_vis":
                users.set_stats_vis(request.form["stats_vis"])
            return redirect(redirect_to)
    else:
        return redirect_to_needs_login() 

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
    return "Page for editing lobby settings and the lobby owner can start the game from here. Not yet implemented."

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
        redirect_to_needs_login()

@app.route("/friends", methods=["GET", "POST"])
def friends():
    if users.is_logged_in():
        if request.method == "GET":
            err_msg = request.args.get("err_msg", "")
            return render_template(
                "friends.html", 
                friends=users.friends_of_user(),
                friend_reqs_in=users.friend_reqs_to_user(),
                friend_reqs_out=users.friend_reqs_from_user(),
                err_msg=err_msg
            )
        if request.method == "POST":
            redirect_to = url_for(".friends")
            if request.form["action"] == "accept_friend_req":
                #It's safe to parse id as an int, because it comes from a hidden field of the form, that the user cannot modify in normal use
                users.accept_friend_req(int(request.form["id"])) 
            elif request.form["action"] == "remove_friend":
                users.remove_friend(int(request.form["id"]))
            elif request.form["action"] == "send_friend_req":
                if len(request.form["username"]) < 2:
                    redirect_to = url_for(".friends", err_msg="Can't send friend request, because username should be at least 2 characters long.") 
                else:
                    result = users.send_friend_req(request.form["username"])
                    if not result.success:
                        #This error message should be converted to error message names as well, so that all the UI related things can be seen in the html
                        redirect_to = url_for(".friends", err_msg=result.result_or_msg) 
            return redirect(redirect_to)
    else:
        redirect_to_needs_login()

@app.route("/error")
def error():
    msg = request.args['msg']
    return render_template("error.html", error_msg=msg)
