from init import db
from flask import session
from random import choice
from enum import Enum
import base64
#User modules
import users

# This module is for db interaction and core logic related to game lobbies
# Lobbies have an integer id that is in the range of an unsigned 24 bit int
# Lobby ids will mostly be passed around as integers, but they also have a base64 representation for use in the urls
# Function names that return or work with the base64 representation will have b64 in their name
def active_games() -> int:
    return db.session.execute("SELECT count(*) FROM lobbies WHERE active").fetchone()[0]

def lobby_id_to_b64(id: int) -> str:
    return base64.urlsafe_b64encode(id.to_bytes(3, byteorder="big")).decode()

def lobby_id_to_int(b64_id: str) -> int:
    return int.from_bytes(base64.urlsafe_b64decode(b64_id), byteorder="big")

def new_lobby(visibility: str) -> int:
    leave_curr_lobby_if_exists()
    used_ids = set(db.session.scalars("SELECT id FROM lobbies"))
    #Id generation takes maybe 0.5 sec even on a fast computer
    lobby_id = choice(tuple(id for id in range(0, 2**24-1) if id not in used_ids))
    sql = """INSERT INTO lobbies (id, owner_id, active, visibility, spectators_allowed) VALUES 
             (:lobby_id, :user_id, True, :visibility, False)"""
    db.session.execute(sql, {"lobby_id": lobby_id, "user_id": session["id"], "visibility": visibility})
    db.session.commit()
    return lobby_id

def leave_lobby(id: int):
    sql = """UPDATE lobbies SET player2_id = NULL WHERE id = :lobby_id"""
    db.session.execute(sql, {"lobby_id": id})
    db.session.commit()

def delete_lobby(id: int):
    sql = """UPDATE lobbies SET active = False WHERE id = :lobby_id"""
    db.session.execute(sql, {"lobby_id": id})
    db.session.commit()

def leave_curr_lobby_if_exists():
    id = owned_lobby_if_exists()
    if id is not None:
        delete_lobby(id)
    else:
        id = owned_lobby_if_exists()
        if id is not None:
            leave_lobby(id)

def join_lobby_as_player(id: int):
    leave_curr_lobby_if_exists()
    sql = "UPDATE lobbies SET player2_id = :user_id WHERE id = :lobby_id"
    db.session.execute(sql, {"user_id": session["id"], "lobby_id": id})
    db.session.commit()

def owned_lobby_if_exists() -> None|int:
    sql = "SELECT id FROM lobbies WHERE active AND owner_id = :user_id"
    return db.session.scalars(sql, {"user_id": session["id"]}).first()
    # It is fine to return the result of the query as is, because callers of this function will expect None if there were no lobbies

def joined_lobby_if_exists() -> None|int:
    sql = "SELECT id FROM lobbies WHERE active AND player2_id = :user_id"
    return db.session.scalars(sql, {"user_id": session["id"]}).first()

def curr_lobby_if_exists() -> None|int:
    id = joined_lobby_if_exists()
    if id is None:
        id = owned_lobby_if_exists()
    return id

def set_lobby_vis(id: int, visibility: str):
    sql = "UPDATE lobbies SET visibility=:visibility WHERE id=:id"
    db.session.execute(sql, {"id":id, "visibility":visibility})
    db.session.commit()

def parse_lobby(lobby: dict) -> dict: # Switch this parser to set status as a bool like the function below
    result = {}
    result["id"] = lobby["id"]
    result["owner_id"] = lobby["owner_id"]
    result["owner"] = users.username_from_id(lobby["owner_id"])
    if lobby["player2_id"] == None:
        result["status"] = "Waiting for player"
    else:
        result["status"] = "Full"
    return result

def get_lobby_status(id: int) -> bool:
    sql = "SELECT player2_id IS NOT NULL FROM lobbies WHERE id = :id"
    return db.session.scalars(sql, {"id": id}).first()

# Friends only lobbies are not yet being filtered out here
def lobby_list() -> map:
    sql = """SELECT id, owner_id, player2_id FROM lobbies
    WHERE active AND visibility != 'private' AND owner_id != :user_id AND (player2_id != :user_id OR player2_id IS NULL)"""
    lobbies_raw = db.session.execute(sql, {"user_id": session["id"]}).all()
    lobbies = [lobby._mapping for lobby in lobbies_raw]
    return map(parse_lobby, lobbies)
