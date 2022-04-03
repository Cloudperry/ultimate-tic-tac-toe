from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome/login page."

@app.route("/account")
def account():
    return "User account settings page."

@app.route("/lobbies")
def lobbies():
    return "Game lobby creation/join page."

#The game/lobby pages will be entered by clicking a button in /lobbies 
#(or by clicking a join link if I implement that)
@app.route("/game/<int:lobby_id>")
def game(lobby_id: int):
    return "Page for playing the game. This will be written in Nim. The clients will communicate to the server via a Websocket url that is specific to the game lobby."

@app.route("/lobby/<int:lobby_id>")
def lobby(lobby_id: int):
    return "Page for editing lobby settings."

@app.route("/stats")
def stats():
    return "Page for showing the user's game history/stats."
