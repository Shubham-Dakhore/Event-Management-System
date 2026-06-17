from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os


# Extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


# ---------------- APP FACTORY ----------------
def create_app():

    app = Flask(__name__, instance_relative_config=True)

    # Configuration
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"


    # Register blueprints
    from .routes.auth import auth
    from .routes.main import main

    app.register_blueprint(auth)
    app.register_blueprint(main)


    return app


# ---------------- LOGIN MANAGER ----------------
from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))