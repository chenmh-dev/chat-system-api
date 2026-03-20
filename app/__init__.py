import os, time, uuid
from flask import Flask, request, g
from .core.db import init_db, close_db
from .core.config import DevelopmentConfig, ProductionConfig
from .core.logging import setup_logging
from .common.errors import register_error_handler
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
            f"duration_ms={duration_ms} user_id={user_id}",
            extra={"request_id": g.request_id}
        )
        return response
    
    app.teardown_appcontext(close_db)

    from .modules.auth.routes import bp as auth
    from .modules.user.routes import bp as user
    from .modules.conversation.routes import bp as conversation
    from .modules.message.routes import bp as message

    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(conversation)
    app.register_blueprint(message)

    register_error_handler(app)
    return app