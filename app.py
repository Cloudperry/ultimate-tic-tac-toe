from flask import redirect, render_template, request, url_for, session, abort
from werkzeug.wrappers.response import Response
from flask_sse import sse
# Modules from this project
from init import app
import users, game_stats, lobbies

def redirect_to_needs_login() -> Response:
    return redirect(url_for(".error", msg="Can't access user stats while not logged in."))

def url_to_lobby(id: int) -> str:
    return url_for("lobby", lobby_id_b64=lobbies.lobby_id_to_b64(id))

def check_csrf():
    if request.form.get("login_token", "") != session["login_token"]:
        abort(403)

@app.route("/")
def index():
    return render_template(
        "index.html",
        logged_in=session.get("id", 0) != 0,
        games_played=game_stats.games_played(),
        active_games=lobbies.active_games()
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        err_name=request.args.get("err_name", "")
        return render_template("login.html", logged_in=session.get("id", 0) != 0, err_name=err_name)
    elif request.method == "POST":
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
        return render_template("register.html", logged_in=users.session.get("id", 0) != 0, err_name=err_name)
    elif request.method == "POST":
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
    if session.get("id", 0) != 0:
        if request.method == "GET":
            return render_template("account.html", logged_in=True, username=users.username(), profile_vis=users.profile_vis()) 
        elif request.method == "POST": 
            check_csrf() #The code below will not get executed if the request is a CSRF attempt
            redirect_to = url_for(".account") #Show account page again if there were no errors
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
            elif request.form["action"] == "set_profile_vis":
                users.set_profile_vis(request.form["profile_vis"])
            return redirect(redirect_to)
    else:
        return redirect_to_needs_login() 

@app.route("/lobby-list", methods=["GET", "POST"])
def play():
    # This page is entirely locked behind login for now
    # It could be changed if I implement spectating games
    if session.get("id", 0): 
        if request.method == "GET":
            lobby_list = lobbies.lobby_list()
            curr_lobby_id, curr_lobby_id_b64 = lobbies.curr_lobby_if_exists(), None
            if curr_lobby_id is not None:
                curr_lobby_id_b64 = lobbies.lobby_id_to_b64(curr_lobby_id)
            return render_template("lobby-list.html", logged_in=True, lobby_list=lobby_list, curr_lobby_id=curr_lobby_id_b64)
        elif request.method == "POST":
            check_csrf()
            redirect_to, lobby_id = "", 0
            if request.form["action"] == "create_lobby":
                lobby_id = lobbies.new_lobby(request.form["visibility"])
                redirect_to = url_to_lobby(lobby_id)
            elif request.form["action"] == "play":
                lobby_id = int(request.form["id"])
                lobbies.join_lobby_as_player(lobby_id)
                redirect_to = url_to_lobby(lobby_id)
            elif request.form["action"] == "spectate":
                redirect_to = url_for(".error", msg="Spectate is not yet implemented.")
            # Send update events over SSE
            if request.form["action"] != "spectate":
                sse.publish({"updated_by": session["id"]}, type="update", channel=f"lobby-{lobby_id}")
                sse.publish({"updated_by": session["id"]}, type="update", channel="lobby-list")
            return redirect(redirect_to)
    else:
        return redirect_to_needs_login()

@app.route("/lobby/<lobby_id_b64>", methods=["GET", "POST"])
def lobby(lobby_id_b64: str):
    lobby_id = lobbies.lobby_id_to_int(lobby_id_b64)
    if session.get("id") is None: 
        return redirect_to_needs_login()
    elif not lobbies.exists(lobby_id):
        return render_template("lobby.html", logged_in=True, exists=False, lobby={"id": lobby_id})
    else:
        lobby_data = lobbies.get_parsed_lobby(lobby_id)
        if request.method == "GET":
            if lobby_data["status"] == lobbies.LobbyStatus.ingame:
                return redirect("/game/" + lobby_id_b64)
            return render_template(
                "lobby.html", 
                logged_in=True, 
                lobby=lobby_data,
                messages=lobbies.get_messages(lobby_id),
                LobbyStatus=lobbies.LobbyStatus
            )
        elif request.method == "POST":
            check_csrf()
            redirect_to = f"/lobby/{lobby_id_b64}"
            if request.form["action"] == "change_vis":
                lobbies.set_lobby_vis(lobby_id, request.form["visibility"])
            elif request.form["action"] == "delete":
                lobbies.delete_lobby(lobby_id)
                redirect_to = "/lobby-list"
            elif request.form["action"] == "leave":
                lobbies.leave_lobby(lobby_id)
                redirect_to = "/lobby-list"
            elif request.form["action"] == "kick":
                lobbies.leave_lobby(lobby_id)
            elif request.form["action"] == "send_msg":
                lobbies.send_msg_in(lobby_id, request.form["content"])
            elif request.form["action"] == "start":
                lobbies.start_game_in(lobby_id)
            # Send update events over SSE
            if request.form["action"] != "change_vis":
                sse.publish({"updated_by": session["id"]}, type="update", channel=f"lobby-{lobby_id}")
            if request.form["action"] != "send_msg":
                sse.publish({"updated_by": session["id"]}, type="update", channel="lobby-list")
            return redirect(redirect_to)

@app.route("/game/<lobby_id>")
def game(lobby_id: str):
    return render_template("game.html", lobby_id=lobby_id, logged_in=session.get("id", 0) != 0)

@app.route("/stats")
def stats():
    if session.get("id", 0) != 0:
        return render_template(
            "stats.html", 
            logged_in=True,
            username=users.username(), 
            game_history=game_stats.user_n_last_games(20),
            games_played=game_stats.user_games_played()
        )
    else:
        redirect_to_needs_login()

@app.route("/friends", methods=["GET", "POST"])
def friends():
    if session.get("id", 0) != 0:
        if request.method == "GET":
            msg_name = request.args.get("msg_name", "")
            return render_template(
                "friends.html", 
                logged_in=True,
                friends=users.friends_of_user(),
                friend_reqs_in=users.friend_reqs_to_user(),
                friend_reqs_out=users.friend_reqs_from_user(),
                msg_name=msg_name
            )
        elif request.method == "POST":
            check_csrf()
            redirect_to = url_for(".friends")
            if request.form["action"] == "accept_friend_req":
                #It's safe to parse id as an int, because it comes from a hidden field of the form, that the user cannot modify in normal use
                users.accept_friend_req(int(request.form["id"])) 
            elif request.form["action"] == "remove_friend":
                users.remove_friend(int(request.form["id"]))
            elif request.form["action"] == "send_friend_req":
                if len(request.form["username"]) < 2:
                    redirect_to = url_for(".friends", msg_name="short_username") 
                if request.form["username"] == users.username():
                    redirect_to = url_for(".friends", msg_name="friend_req_to_self") 
                else:
                    result = users.send_friend_req(request.form["username"])
                    if not result.success:
                        redirect_to = url_for(".friends", msg_name=result.result_or_msg) 
            return redirect(redirect_to)
    else:
        redirect_to_needs_login()

@app.route("/error")
def error():
    msg = request.args['msg']
    return render_template("error.html", error_msg=msg)
