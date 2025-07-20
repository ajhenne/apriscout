"""Initialize the Apriscout Flask application.

Sets up the application factory pattern, configures the database and login manager.
"""

import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

load_dotenv()


def create_app(test_config=None):
    """Create and return the Flask application object."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    if test_config is not None:
        app.config.update(test_config)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    _ = Migrate(app, db)

    from .routes import main
    from .routes_apritable import main as main_apritable

    app.register_blueprint(main)
    app.register_blueprint(main_apritable)

    app.jinja_env.globals["attribute"] = getattr

    return app
