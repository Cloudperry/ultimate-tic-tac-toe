from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sse import sse
from os import getenv, environ
from dotenv import load_dotenv
# Modules from this project
from generate_secret_key import generate_key_if_not_exist
from games import Games

# Initialize Flask app
app = Flask(__name__)
load_dotenv()
if 'HEROKU' not in environ:
    generate_key_if_not_exist()
app.secret_key = getenv("SECRET_KEY")
# Initialize db
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
# Initialize server-sent events
app.config["REDIS_URL"] = getenv("REDIS_URL")
app.register_blueprint(sse, url_prefix='/updates')
# Reset all lobbies that were in game when the app was restarted (game state doesn't survive restarts)
db.session.execute("UPDATE lobbies SET status = 'ready' WHERE status = 'ingame'")
db.session.commit() 
game_list = Games() # Initialize class that stores game state objects for each lobby id with an active game
