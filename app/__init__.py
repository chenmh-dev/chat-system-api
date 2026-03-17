import os
from flask import Flask
from .db import init_db, close_db
from .errors import registe_error_hanlder
from .config import DevelopmentConfig, ProductionConfig
def create_app():
    app = Flask(__name__)
    env = os.getenv("APP_ENV", "development").lower()
    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    init_db()
    
    app.teardown_appcontext(close_db)

    from .routes import bp as home
    from .blueprints.auth_routes import bp as auth
    from .blueprints.user_routes import bp as user

    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(user)

    registe_error_hanlder(app)
    return app