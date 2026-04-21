from decouple import config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import DevelopmentConfig
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt
from flask_cors import CORS
apps=Flask(__name__)
CORS(apps,origins=["http://localhost:5173"])
login_manager=LoginManager()
login_manager.init_app(apps)
bcrypt=Bcrypt(apps)
db = SQLAlchemy()
migrate = Migrate()
jwt=JWTManager()
apps.config.from_object(DevelopmentConfig)

jwt.init_app(apps)
db.init_app(apps)
migrate.init_app(apps, db)
from app.accounts.views import accounts_bp
from app.core.view import core_bp

apps.register_blueprint(accounts_bp)
apps.register_blueprint(core_bp)

from app.accounts.models import User

login_manager.login_view = "accounts.login"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()