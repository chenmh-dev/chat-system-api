from flask import Blueprint, request
from ..validators.common_validators import get_json, required_str
from ..services import auth_service
from ..response import ok
bp = Blueprint("auth", __name__)

@bp.post("/register")
def register_route():
    data = get_json(request=request)
    username = required_str(data, "username", min_len=1, max_len=100)
    password = required_str(data, "password", min_len=2, max_len=200)
    result = auth_service.register(username=username, password=password)
    return ok(data=result, message="Register success", status=200)

@bp.post("/login")
def login_route():
    data = get_json(request=request)
    username = required_str(data, "username", min_len=1, max_len=100)
    password = required_str(data, "password", min_len=2, max_len=200)
    result = auth_service.login(username, password)
    return ok(data=result, message="Login success", status=200)
