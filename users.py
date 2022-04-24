from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from init import db

def login(username: str, password: str) -> bool:
    sql = "SELECT id, password FROM users WHERE username=:username"
    user = db.session.execute(sql, {"username":username}).fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False

def update_password(old_password: str, password: str) -> bool:
    sql = "SELECT id, password FROM users WHERE id=:id"
    user = db.session.execute(sql, {"id":user_id()}).fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, old_password):
            password_hash = generate_password_hash(password)
            sql = "UPDATE users SET password=:password WHERE id=:id"
            db.session.execute(sql, {"id":user.id, "password":password_hash})
            db.session.commit()
            return True
        else:
            return False

def set_stats_vis(visibility: str) -> bool:
    sql = "SELECT id, password FROM users WHERE id=:id"
    user = db.session.execute(sql, {"id":user_id()}).fetchone()
    if not user:
        return False
    else:
        sql = "UPDATE users SET stats_visibility=:stats_vis WHERE id=:id"
        db.session.execute(sql, {"id":user.id, "stats_vis":visibility})
        db.session.commit()
        return True

def stats_vis() -> str:
    sql = "SELECT stats_visibility FROM users WHERE id=:id"
    return db.session.execute(sql, {"id":user_id()}).fetchone()[0]

def logout():
    del session["user_id"]

def register(username: str, password: str) -> bool:
    password_hash = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password,stats_visibility) VALUES (:username,:password,'private')"
        db.session.execute(sql, {"username":username, "password":password_hash})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id() -> int:
    return session.get("user_id", 0)

def is_logged_in():
    return user_id() != 0
