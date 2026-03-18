from ..db import get_db

def get_user_by_id(user_id: int) -> dict | None:
    db = get_db()
    row = db.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    return dict(row) if row else None
