import os, time, uuid
from flask import Flask, request, g
from .db import init_db, close_db
from .errors import registe_error_hanlder
from .config import DevelopmentConfig, ProductionConfig
from .utils.logging import setup_logging
def create_app():
    app = Flask(__name__)
    env = os.getenv("APP_ENV", "development").lower()
    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    setup_logging(app=app)

    init_db()
    
    @app.before_request
    def _start_timer_and_request_id():
        g.start_time = time.time()
        g.request_id = uuid.uuid4().hex[:12]
    
    @app.after_request
    def _log_request(response):
        duration_ms = int((time.time() - getattr(g, "start_time", time.time()))*1000)
        user_id = None
        if hasattr(g, "user") and isinstance(g.user, dict):
            user_id = g.user.get("user_id")
        
        response.headers["X-Request-Id"] = g.request_id

        app.logger.info(
            f"{request.method} {request.path} status={response.status_code} "
            f"duration_mc={duration_ms} user_id={user_id}",
            extra={"request_id": g.request_id}
        )
        return response
    
    app.teardown_appcontext(close_db)

    from .routes import bp as home
    from .blueprints.auth_routes import bp as auth
    from .blueprints.user_routes import bp as user
    from .blueprints.conversation_routes import bp as conversation
    from .blueprints.message_routes import bp as message
    
    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(conversation)
    app.register_blueprint(message)

    registe_error_hanlder(app)
    return app