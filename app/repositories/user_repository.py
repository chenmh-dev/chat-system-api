from ..db import get_db
    
# def username_exists(username: str) -> bool:
#     db = get_db()
#     row = db.execute(
#         "SELECT id FROM users WHERE username = ?",
#         (username,)
#     ).fetchone()
#     return True if row else False

def create_user(username: str, password_hash: str):
    db = get_db()
    cur = db.execute(
        "INSERT INTO users (username, password) VALUES(?, ?)",
        (username, password_hash)
    )
    db.commit()
    return cur.lastrowid

def get_user_by_username(username: str) -> dict | None:
    db = get_db()
    row = db.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    return dict(row) if row else None

def get_user_by_id(user_id: int) -> dict | None:
    db = get_db()
    row = db.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    return dict(row) if row else None
