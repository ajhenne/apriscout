"""Test apritable functions."""

import pytest

from apriscout import db
from apriscout.models import UserPokemon


def test_apritable_public_access(client):
    """Ensure anyone can view a user's collection page."""
    response = client.get("/existing_user_1")
    assert response.status_code == 200
    assert b"existing_user_1" in response.data


@pytest.fixture
def logged_in_client(client, app):
    """Log in as existing_user_1 using session manipulation."""
    with client.session_transaction() as session:
        session["_user_id"] = "1"
    return client


def test_apritable_post_updates(logged_in_client, app):
    """Test that toggling a checkbox saves the update."""
    with app.app_context():
        up = UserPokemon(user_id=1, pokemon_id=102)  # Arcanine
        db.session.add(up)
        db.session.commit()

        response = logged_in_client.post(
            "/existing_user_1",
            data={f"toggle_{up.id}_fast": "on"},
            follow_redirects=True,
        )
        assert b"Collection updated successfully" in response.data

        updated = db.session.get(UserPokemon, up.id)
        assert updated.fast is True


def test_apritable_checkbox_uncheck(logged_in_client, app):
    """Test that removing a checked box resets it to False."""
    with app.app_context():
        up = UserPokemon(user_id=1, pokemon_id=102, fast=True)
        db.session.add(up)
        db.session.commit()

        response = logged_in_client.post(
            "/existing_user_1",
            data={},
            follow_redirects=True,
        )
        assert b"Collection updated successfully" in response.data

        updated = db.session.get(UserPokemon, up.id)
        assert updated.fast is False


def test_apritable_invalid_user(client):
    """Ensure a nonexistent username returns 302 and redirects home."""
    response = client.get("/nonexistent_user", follow_redirects=True)
    assert b"User not found" in response.data
