from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from init import db
from collections import namedtuple
from secrets import token_hex

Result = namedtuple("Result", ["success", "result_or_msg"])

def login(username: str, password: str) -> bool:
    sql = "SELECT id, password FROM users WHERE username=:username"
    user = db.session.execute(sql, {"username":username}).fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["login_token"] = token_hex(16)
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
    sql = "UPDATE users SET stats_visibility=:stats_vis WHERE id=:id"
    db.session.execute(sql, {"id":user_id(), "stats_vis":visibility})
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

def id_from_username_if_exists(username: str) -> Result:
    sql = "SELECT id FROM users WHERE username=:username"
    try:
        return Result(True, db.session.execute(sql, {"username":username}).fetchone()[0])
    except:
        return Result(False, f"invalid_username")

def username_from_id(id: int) -> int:
    sql = "SELECT username FROM users WHERE id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()[0]

def username() -> int:
    return username_from_id(user_id())

def user_id() -> int:
    return session.get("user_id", 0)

def is_logged_in():
    return user_id() != 0

User = namedtuple("User", ["id", "name"])

def friends_of_user():
    sql = """SELECT CASE
WHEN sender_id=:id THEN recipient_id 
ELSE sender_id END
FROM friends WHERE (sender_id=:id OR recipient_id=:id) AND accepted"""
    friend_ids = db.session.execute(sql, {"id":user_id()}).fetchall()
    return map(lambda id: User(id[0], username_from_id(id[0])), friend_ids)

def friend_reqs_to_user():
    sql = "SELECT sender_id FROM friends WHERE recipient_id=:id AND NOT accepted"
    friend_ids = db.session.execute(sql, {"id":user_id()}).fetchall()
    return map(lambda id: User(id[0], username_from_id(id[0])), friend_ids)

def friend_reqs_from_user():
    sql = "SELECT recipient_id FROM friends WHERE sender_id=:id AND NOT accepted"
    friend_ids = db.session.execute(sql, {"id":user_id()}).fetchall()
    return map(lambda id: User(id[0], username_from_id(id[0])), friend_ids)

def send_friend_req(to_username: str) -> Result:
    to_id = id_from_username_if_exists(to_username)
    if to_id.success:
        try:
            sql = "INSERT INTO friends (sender_id, recipient_id, accepted) VALUES (:from_id, :to_id, False)"
            db.session.execute(sql, {"from_id": user_id(), "to_id": to_id.result_or_msg})
            db.session.commit()
            return Result(True, "friend_req_sent")
        except:
            return Result(False, "friend_or_req_exists")
    else:
        return to_id

def accept_friend_req(accept_id: int):
    sql = "UPDATE friends SET accepted = True WHERE sender_id=:accept_id AND recipient_id=:user_id OR sender_id=:user_id AND recipient_id=:accept_id"
    db.session.execute(sql, {"user_id": user_id(), "accept_id": accept_id})
    db.session.commit()

def remove_friend(remove_id: int):
    sql = "DELETE FROM friends WHERE sender_id=:remove_id AND recipient_id=:user_id OR sender_id=:user_id AND recipient_id=:remove_id"
    db.session.execute(sql, {"user_id": user_id(), "remove_id": remove_id})
    db.session.commit()
