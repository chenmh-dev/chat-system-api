from flask import Flask
from werkzeug.exceptions import HTTPException
from .exceptions import AppError
from .utils import fail

def registe_error_hanlder(app: Flask):

    @app.errorhandler(AppError)
    def handel_app_error(err):
        return fail(code=err.code, message=err.message, status=err.status)

    @app.errorhandler(HTTPException)
    def handel_unexpected_error(err):
        import traceback
        traceback.print_exc()
        return fail(code="INTERNAL_ERROR", message="Internal server error", status=500)