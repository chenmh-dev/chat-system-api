from functools import wraps
from flask import request, g
from .auth import verify_auth_token
from .exceptions import Unauthorized
def require_auth_token(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "").strip()

        if not auth.startswith("Bearer "):
            raise Unauthorized(message="Missing Bearer token")
        token = auth.removeprefix("Bearer ").strip()
        data = verify_auth_token(token=token)
        if data is None or "user_id" not in data:
            raise Unauthorized(message="Ivalid token or expired")
        g.user = data
        return fn(*args, **kwargs)
    return wrapper