from init import db
import users

#Here I will add code related to stats about past games (from table game_stats)
#Code for personal stats like winrate and games history will also be added here 

def game_count() -> int:
    return db.session.execute("SELECT count(*) FROM game_stats").fetchone()[0]

def user_game_count() -> int: #This function hasn't been tested yet
    sql = "SELECT count(*) FROM game_stats WHERE user_id=:id"
    return db.session.execute(sql, {"id":users.user_id()}).fetchone()[0]

