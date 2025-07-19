from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from apriscout import db
from apriscout.constants import apriball_names
from apriscout.models import CustomCategory, Pokemon, User, UserPokemon
from apriscout.services import update_user_collection

bp = Blueprint("apri", __name__)


@bp.route("/<username>", methods=["GET", "POST"])
def apritable(username):
    """Render the profile page for a given username."""
    user = User.query.filter(func.lower(User.username) == username.lower()).first()

    if not user:
        flash("User not found.")
        return redirect(url_for("main.home"))

    can_edit = current_user.is_authenticated and current_user.id == user.id

    if request.method == "POST" and can_edit:
        updated = update_user_collection(user, request.form)

        if updated:
            db.session.commit()
            flash("Collection updated successfully.")
        else:
            flash("No changes made.")
        return redirect(url_for("main.apritable", username=username))

    all_pokemon = [
        {"id": p.id, "name": p.name, "sprite": p.sprite}
        for p in Pokemon.query.order_by(Pokemon.name).all()
    ]

    user_collection = UserPokemon.query.filter_by(user_id=user.id).join(Pokemon).all()
    user_categories = [
        cat.name for cat in CustomCategory.query.filter_by(user_id=user.id).all()
    ]
    unique_combinations = sum(
        sum(1 for ball in apriball_names if getattr(entry, ball))
        for entry in user_collection
    )
    completed_pokemon = sum(
        all(getattr(entry, ball) for ball in apriball_names)
        for entry in user_collection
    )
    total_progress = round(unique_combinations / (len(all_pokemon) * 9) * 100, 1)

    return render_template(
        "apritable.html",
        user=user,
        can_edit=can_edit,
        all_pokemon=all_pokemon,
        collection=user_collection,
        user_categories=user_categories,
        unique_combinations=unique_combinations,
        completed_pokemon=completed_pokemon,
        total_progress=total_progress,
        ball_list=apriball_names,
    )


@bp.route("/<username>/add_pokemon", methods=["POST"])
@login_required
def add_pokemon(username):
    """Add a Pokemon to the user's Apritable."""

    user = User.query.filter(func.lower(User.username) == username.lower()).first()
    if not user:
        flash("User not found.", category="error")
        return redirect(url_for("main.home"))

    if current_user.id != user.id:
        flash(
            "You are not authorised to edit someone else's collection.",
            category="error",
        )

    pokemon_id = request.form.get("pokemon_id")
    if not pokemon_id:
        flash("Invalid Pokemon selection.", category="warning")
        return redirect(url_for("main.apritable", username=username))

    already_exists = UserPokemon.query.filter_by(
        user_id=user.id,
        pokemon_id=pokemon_id,
    ).first()
    if already_exists:
        flash("That Pokemon already exists in your collection.", category="warning")
    else:
        new_entry = UserPokemon(user_id=user.id, pokemon_id=pokemon_id)
        db.session.add(new_entry)
        db.session.commit()
        flash(
            f"{Pokemon.query.get(pokemon_id).name} added to your collection!",
            category="success",
        )

    return redirect(url_for("main.apritable", username=username))
