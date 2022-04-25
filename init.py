from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv, environ
from generate_secret_key import generate_key_if_not_exist

app = Flask(__name__)

generate_key_if_not_exist()
if 'HEROKU' not in environ:
    app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
