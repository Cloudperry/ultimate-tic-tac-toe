from init import db
from flask import session
import users

#Here I will add code related to stats about past games (from table game_stats)
#Code for personal stats like winrate and games history will also be added here 

def games_played() -> int:
    return db.session.execute("SELECT count(*) FROM game_stats").fetchone()[0]

def user_games_played() -> int: #This function hasn't been tested yet
    sql = "SELECT count(*) FROM game_stats WHERE winner_id=:id OR loser_id=:id"
    return db.session.execute(sql, {"id":session["id"]}).fetchone()[0]

def parse_game_for_user(game: dict) -> dict:
    result = {}
    if game["winner_id"] == session["id"]:
        result["result"] = "win"
        result["opponent"] = users.username_from_id(game["loser_id"])
    else:
        result["result"] = "loss"
        result["opponent"] = users.username_from_id(game["winner_id"])
    result["move_count"] = game["move_count"]
    result["played_on"] = game["played_on"]
    return result

def user_n_last_games(n: int):
    sql = "SELECT * FROM game_stats WHERE winner_id=:id OR loser_id=:id ORDER BY played_on"
    games_raw = db.session.execute(sql, {"id":session["id"]}).all()
    games = [qr._mapping for qr in games_raw]
    return list(map(parse_game_for_user, games))
