from init import db
from random import choice
import base64
#User modules
import users

#Here I will add code related to managing game lobbies and messages
#Retrieving stats about active games will also be added here
def active_games() -> int:
    return db.session.execute("SELECT count(*) FROM lobbies WHERE active").fetchone()[0]

def lobby_id_to_b64(id: int) -> str:
    return base64.urlsafe_b64encode(id.to_bytes(3, byteorder='big')).decode()

def new_lobby(visibility: str) -> str:
    used_ids = set(db.session.scalars("SELECT id FROM lobbies"))
    #Id generation takes maybe 0.5 sec even on a fast computer
    lobby_id = choice(tuple(id for id in range(0, 2**24-1) if id not in used_ids))
    sql = """INSERT INTO lobbies (id, owner_id, active, visibility, spectators_allowed) VALUES 
             (:lobby_id, :user_id, True, :visibility, False)"""
    db.session.execute(sql, {"lobby_id": lobby_id, "user_id": users.user_id(), "visibility": visibility})
    db.session.commit()
    return lobby_id_to_b64(lobby_id)

def join_lobby_as_player(id: int):
    sql = "UPDATE lobbies SET player2_id = :user_id WHERE id = :id"
    db.session.execute(sql, {"user_id": users.user_id(), "id": id})
    db.session.commit()

def parse_lobby(lobby: dict) -> dict:
    result = {}
    result["id"] = lobby_id_to_b64(lobby["id"])
    result["owner"] = users.username_from_id(lobby["owner_id"])
    if lobby["player2_id"] == None:
        result["status"] = "Waiting for player"
    else:
        result["status"] = "Full"
    return result

def owned_lobby_if_exists() -> None|str:
    sql = "SELECT id FROM lobbies WHERE active AND owner_id = :user_id"
    lobby_id = db.session.scalars(sql, {"user_id": users.user_id()}).first()
    if lobby_id is not None:
        return lobby_id_to_b64(lobby_id)

def lobby_list() -> map:
    lobbies_raw = db.session.execute("SELECT id, owner_id, player2_id FROM lobbies WHERE active AND visibility != 'private'").all()
    lobbies = [lobby._mapping for lobby in lobbies_raw]
    return map(parse_lobby, lobbies)
