import pytest
from werkzeug.security import generate_password_hash

from apriscout import create_app, db
from apriscout.models import User


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",  # in-memory
        }
    )
    with app.app_context():
        db.create_all()

        # Populate with existing user.
        existing_user = User(
            username="existing_user",
            email="existing@apriscout.com",
            password_hash=generate_password_hash("athios"),
        )
        db.session.add(existing_user)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
