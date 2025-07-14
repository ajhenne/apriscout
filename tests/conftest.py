"""Pytest configuration and fixtures for apriscout tests."""

import pytest
from werkzeug.security import generate_password_hash

from apriscout import create_app, db
from apriscout.models import Pokemon, User


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

        # Populate User table with some test existing users.
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

        # Populate Pokemon table with a few Pokemon.
        pokemon_entries = [
            Pokemon(
                id=102,
                name="Arcanine",
                sprite="sprites/pokemon/102.png",
                generation=1,
                type1="fire",
                type2=None,
                dex_num=59,
                form_id=None,
                is_female=False,
            ),
            Pokemon(
                id=869,
                name="Swanna",
                sprite="sprites/pokemon/869.png",
                generation=5,
                type1="water",
                type2=None,
                dex_num=581,
                form_id=None,
                is_female=False,
            ),
            Pokemon(
                id=1241,
                name="Thievul",
                sprite="sprites/pokemon/1241.png",
                generation=8,
                type1="dark",
                type2=None,
                dex_num=828,
                form_id=None,
                is_female=False,
            ),
        ]

        db.session.add_all(pokemon_entries)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Return a Flask test client for the given app fixture."""
    return app.test_client()
