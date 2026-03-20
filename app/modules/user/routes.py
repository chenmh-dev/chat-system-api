from flask import Blueprint, g
from ...common.decorators import require_auth_token
from ...common.response import ok
from . import service as user_svc

bp = Blueprint("user", __name__)

@bp.get("/me")
@require_auth_token
def me():
    user_id = g.user["user_id"]
    result = user_svc.get_user(user_id=user_id)  
    return ok(data=result, message="Me", status=200)
