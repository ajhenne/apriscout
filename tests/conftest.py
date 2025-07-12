"""Pytest configuration and fixtures for apriscout tests."""

import pytest
from werkzeug.security import generate_password_hash

from apriscout import create_app, db
from apriscout.models import User


@pytest.fixture
def app():
    """Yield a Flask app instance for tests."""
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",  # in-memory
        },
    )
    with app.app_context():
        db.create_all()

        # Populate with existing user.
        existing_user_1 = User(
            username="existing_user_1",
            email="existing_1@apriscout.com",
            password_hash=generate_password_hash("athios"),
        )
        existing_user_2 = User(
            username="existing_user_2",
            email="existing_2@apriscout.com",
            password_hash=generate_password_hash("kratos"),
        )
        db.session.add(existing_user_1)
        db.session.add(existing_user_2)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Return a Flask test client for the given app fixture."""
    return app.test_client()
