"""
Auth Service — Flask
Handles user registration, login, JWT issuance, and profile management.
User model is merged here (no separate User Service).
"""
from flask import Flask
from app.db.database import db, migrate
from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp
from app.core.config import Config
import logging

logging.basicConfig(level=logging.INFO)


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(user_bp, url_prefix="/api/v1/users")

    @app.get("/health")
    def health():
        return {"status": "UP", "service": "auth-service"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
