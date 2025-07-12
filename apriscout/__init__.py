from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test-secret"

    if test_config is not None:
        app.config.update(test_config)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    from .routes import main

    app.register_blueprint(main)

    return app
