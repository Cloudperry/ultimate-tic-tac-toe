from init import db
from flask import session
# Modules from this project
import users

#Here I will add code related to stats about past games (from table game_stats)
#Code for personal stats like winrate and games history will also be added here 

def games_played() -> int:
    return db.session.scalars("SELECT count(*) FROM game_stats").first()

def user_games_played() -> int: #This function hasn't been tested yet
    sql = "SELECT count(*) FROM game_stats WHERE winner_id=:id OR loser_id=:id"
    return db.session.scalars(sql, {"id":session["id"]}).first()

def user_games_won() -> int: #This function hasn't been tested yet
    sql = "SELECT count(*) FROM game_stats WHERE winner_id=:id"
    return db.session.scalars(sql, {"id":session["id"]}).first()

def parse_game_for_user(game: dict) -> dict:
    result = {}
    if game["winner_id"] == session["id"]:
        result["is_win"] = True
        result["opponent"] = users.username_from_id(game["loser_id"])
    else:
        result["is_win"] = False
        result["opponent"] = users.username_from_id(game["winner_id"])
    result["move_count"] = game["move_count"]
    result["played_on"] = game["played_on"]
    return result

def user_n_last_games(n: int):
    sql = "SELECT winner_id, loser_id, to_char(played_on, 'DD/MM/YYYY HH24:MI:SS') AS played_on, move_count FROM game_stats WHERE winner_id=:id OR loser_id=:id ORDER BY played_on"
    games_raw = db.session.execute(sql, {"id":session["id"]}).all()
    games = [qr._mapping for qr in games_raw]
    return list(map(parse_game_for_user, games))

def add_game(winner_id: int, loser_id: int, move_count: int):
    sql = "INSERT INTO game_stats (winner_id, loser_id, move_count, played_on) VALUES (:winner_id, :loser_id, :move_count, current_timestamp)"
    db.session.execute(sql, {"winner_id": winner_id, "loser_id": loser_id, "move_count": move_count})
    db.session.commit()
