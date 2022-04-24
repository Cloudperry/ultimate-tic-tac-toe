from init import db

#Here I will add code related to managing game lobbies and messages
#Retrieving stats about active games will also be added here
def active_games() -> int:
    return db.session.execute("SELECT count(*) FROM lobbies WHERE active").fetchone()[0]
