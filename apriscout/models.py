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

    collections = db.relationship(
        "UserPokemon", back_populates="user", cascade="all, delete-orphan",
    )

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


class Pokemon(db.Model):
    """Master table of Pokemon and details.

    Attributes:
        id (int): Internal unique ID for each Pokemon.
        name (str): Pokemon name.
        dexNum (int): Pokedex number.
        formId (str): Special forms, like female or gimicks.
        smogon (str): Smogon name.
        isFemale (bool): If the Pokemon is (specifically) female.
        hiddenAbility (bool): If the Pokemon has a hidden ability.
        abilities (str): The Pokemon's hidden ability, or otherwise first ability.
        sprite (str): The link to the Pokemon's sprite.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    dex_num = db.Column(db.Integer)
    form_id = db.Column(db.String(10))
    is_female = db.Column(db.Boolean)
    generation = db.Column(db.Integer)
    type1 = db.Column(db.String(10))
    type2 = db.Column(db.String(10))
    sprite = db.Column(db.String(255))


class UserPokemon(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey("pokemon.id"), nullable=False)

    ball_fast = db.Column(db.Boolean, default=False)
    ball_lure = db.Column(db.Boolean, default=False)
    ball_level = db.Column(db.Boolean, default=False)
    ball_heavy = db.Column(db.Boolean, default=False)
    ball_love = db.Column(db.Boolean, default=False)
    ball_moon = db.Column(db.Boolean, default=False)
    ball_dream = db.Column(db.Boolean, default=False)
    ball_beast = db.Column(db.Boolean, default=False)
    ball_safari = db.Column(db.Boolean, default=False)
    ball_sport = db.Column(db.Boolean, default=False)

    user = db.relationship("User", back_populates="collections")
    pokemon = db.relationship("Pokemon")
