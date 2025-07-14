from . import db
from .constants import apriball_names
from .models import UserPokemon


def update_user_collection(user, form_data):
    """Update a user's Pokémon collection based on submitted form data.

    Args:
        user (User): The user whose collection is being updated.
        form_data (ImmutableMultiDict): The submitted form data.

    Returns:
        bool: True if any changes were made, False otherwise.
    """
    updated = False

    for key in form_data:
        if key.startswith("toggle_"):
            parts = key.split("_")
            if len(parts) == 3:
                pokemon_id = int(parts[1])
                ball = parts[2]
                user_pokemon = db.session.get(UserPokemon, pokemon_id)
                if user_pokemon and user_pokemon.user_id == user.id:
                    current_value = getattr(user_pokemon, ball, None)
                    if current_value is not True:
                        setattr(user_pokemon, ball, True)
                        updated = True

    for entry in UserPokemon.query.filter_by(user_id=user.id).all():
        for ball in apriball_names:
            field_name = f"toggle_{entry.id}_{ball}"
            if field_name not in form_data and getattr(entry, ball):
                setattr(entry, ball, False)
                updated = True

    return updated
