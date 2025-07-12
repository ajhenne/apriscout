"""Defines the database models for apriscout."""

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager


class User(db.Model, UserMixin):
    """Represents a user account in the Apriscout application.

    Attributes:
        id (int): Primary key, unique user identifier.
        username (str): Unique username.
        email (str): Unique email address.
        password_hash (str): Password stored as a hash.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """Hash and set a password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check the plaintext password against hashed password."""
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    """Return the user instance."""
    return User.query.get(int(user_id))
