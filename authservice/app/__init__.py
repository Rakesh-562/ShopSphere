from decouple import config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import DevelopmentConfig

apps=Flask(__name__)
login_manager=LoginManager()
login_manager.init_app(apps)
bcrypt=Bcrypt(apps)
db = SQLAlchemy()
migrate = Migrate()
apps.config.from_object(DevelopmentConfig)

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