from init import db
from flask import session
from random import choice
from enum import Enum
import base64
# Modules from this project
import users

# This module is for db interaction and core logic related to game lobbies
# Lobbies have an integer id that is in the range of an unsigned 24 bit int
# Lobby ids will mostly be passed around as integers, but they also have a base64 representation for use in the urls
# Function names that return or work with the base64 representation will have b64 in their name
def active_games() -> int:
    return db.session.execute("SELECT count(*) FROM lobbies WHERE status != 'inactive'").fetchone()[0]

def lobby_id_to_b64(id: int) -> str:
    return base64.urlsafe_b64encode(id.to_bytes(3, byteorder="big")).decode()

def lobby_id_to_int(b64_id: str) -> int:
    return int.from_bytes(base64.urlsafe_b64decode(b64_id), byteorder="big")

def new_lobby(visibility: str) -> int:
    leave_curr_lobby_if_exists()
    used_ids = set(db.session.scalars("SELECT id FROM lobbies"))
    #Id generation takes maybe 0.5 sec even on a fast computer
    lobby_id = choice(tuple(id for id in range(0, 2**24-1) if id not in used_ids))
    sql = """INSERT INTO lobbies (id, owner_id, status, visibility, spectators_allowed) VALUES 
             (:lobby_id, :user_id, 'waiting', :visibility, False)"""
    db.session.execute(sql, {"lobby_id": lobby_id, "user_id": session["id"], "visibility": visibility})
    db.session.commit()
    return lobby_id

def leave_lobby(id: int):
    sql = """UPDATE lobbies SET player2_id = NULL, status = 'waiting' WHERE id = :lobby_id"""
    db.session.execute(sql, {"lobby_id": id})
    db.session.commit()

def delete_lobby(id: int):
    sql = """UPDATE lobbies SET status = 'inactive' WHERE id = :lobby_id"""
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
    sql = "UPDATE lobbies SET player2_id = :user_id, status = 'ready' WHERE id = :lobby_id"
    db.session.execute(sql, {"user_id": session["id"], "lobby_id": id})
    db.session.commit()

def owned_lobby_if_exists() -> None|int:
    sql = "SELECT id FROM lobbies WHERE status != 'inactive' AND owner_id = :user_id"
    return db.session.scalars(sql, {"user_id": session["id"]}).first()
    # It is fine to return the result of the query as is, because callers of this function will expect None if there were no lobbies

def joined_lobby_if_exists() -> None|int:
    sql = "SELECT id FROM lobbies WHERE status != 'inactive' AND player2_id = :user_id"
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

class LobbyStatus(Enum):
    ingame = 1
    ready = 2 
    waiting = 3
    inactive = 4

def parse_lobby_for_list(lobby: dict) -> dict:
    return parse_lobby(lobby, for_lobby_list=True)

def parse_lobby(lobby: dict, for_lobby_list=False) -> dict:
    result = {}
    result["owner_id"] = lobby["owner_id"]
    result["owner"] = users.username_from_id(lobby["owner_id"])
    result["player2_id"] = lobby["player2_id"]
    result["player2"] = users.username_from_id(lobby["owner_id"])
    result["id_b64"] = lobby_id_to_b64(lobby["id"])
    result["id"] = lobby["id"]
    if not for_lobby_list:
        result["status"] = LobbyStatus[lobby["status"]]
    return result

def get_parsed_lobby(id: int) -> dict:
    sql = "SELECT id, owner_id, player2_id, status FROM lobbies WHERE id = :id"
    lobby = db.session.execute(sql, {"id": id}).one()
    return parse_lobby(lobby._mapping)

# Friends only lobbies are not yet being filtered out here
def lobby_list() -> map:
    sql = """SELECT id, owner_id, player2_id, status FROM lobbies
    WHERE status != 'inactive' AND visibility != 'private' AND owner_id != :user_id AND (player2_id != :user_id OR player2_id IS NULL)"""
    lobbies_raw = db.session.execute(sql, {"user_id": session["id"]}).all()
    lobbies = [lobby._mapping for lobby in lobbies_raw]
    return map(parse_lobby_for_list, lobbies)

def get_messages(id: int):
    sql = """SELECT u.username, m.content, to_char(m.sent_at, 'DD/MM/YYYY HH24:MI:SS') AS sent_at
    FROM users u, messages m 
    WHERE m.lobby_id = :id AND m.user_id = u.id ORDER BY m.sent_at"""
    messages_raw = db.session.execute(sql, {"id": id}).all()
    messages = [message._mapping for message in messages_raw]
    return messages

def send_msg_in(id: int, content: str):
    sql = """INSERT INTO messages (lobby_id, user_id, content, sent_at) VALUES (:lobby_id, :user_id, :content, current_timestamp)"""
    db.session.execute(sql, {"lobby_id": id, "user_id": session["id"], "content": content})
    db.session.commit()

def start_game_in(id: int):
    sql = "UPDATE lobbies SET status = 'ingame' WHERE id=:id"
    db.session.execute(sql, {"id": id})
    db.session.commit()

def exists(id: int) -> bool:
    sql = "SELECT True FROM lobbies WHERE id = :id"
    return db.session.execute(sql, {"id": id}).fetchone() is not None
