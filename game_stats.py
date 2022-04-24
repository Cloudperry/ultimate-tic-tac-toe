from init import db
import users

#Here I will add code related to stats about past games (from table game_stats)
#Code for personal stats like winrate and games history will also be added here 

def games_played() -> int:
    return db.session.execute("SELECT count(*) FROM game_stats").fetchone()[0]

def user_games_played() -> int: #This function hasn't been tested yet
    sql = "SELECT count(*) FROM game_stats WHERE player1=:id OR player2=:id"
    return db.session.execute(sql, {"id":users.user_id()}).fetchone()[0]

def user_n_last_games(n: int):
    sql = "SELECT * FROM game_stats WHERE player1=:id OR player2=:id ORDER BY played_on"
    return db.session.execute(sql, {"id":users.user_id()}).fetchall()
