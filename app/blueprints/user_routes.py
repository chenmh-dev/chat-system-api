from flask import Blueprint, g
from ..decorators import require_auth_token
from ..response import ok
from ..services import user_service

bp = Blueprint("user", __name__)

@bp.get("/me")
@require_auth_token
def me():
    user_id = g.user["user_id"]
    result = user_service.get_user(user_id=user_id)  
    return ok(data=result, message="Me", status=200)
