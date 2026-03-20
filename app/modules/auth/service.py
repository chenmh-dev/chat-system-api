from werkzeug.security import generate_password_hash, check_password_hash
from ...common.exceptions import  LoginFailed, UserExists
from ...common.auth import generate_auth_token
from ..user import repository as user_repo

def register(username: str, password: str) -> dict:
    if user_repo.get_user_by_username(username=username):
        raise UserExists()
    password_hash = generate_password_hash(password)
    user_id = user_repo.create_user(username=username, password_hash=password_hash)
    return {"user_id": user_id, "username": username}

def login(username: str, password: str) -> dict:

    user = user_repo.get_user_by_username(username=username)
    if not user:
        raise LoginFailed()
    if not check_password_hash(user["password"], password):
        raise LoginFailed()
    token = generate_auth_token({"user_id": user["id"]})
    return {"user": user, "token": token}
