from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from apriscout import db
from apriscout.constants import apriball_names
from apriscout.models import CustomCategory, Pokemon, User, UserPokemon
from apriscout.services import update_user_collection

main = Blueprint("apri", __name__)


@main.route("/<username>", methods=["GET", "POST"])
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
        return redirect(url_for("apri.apritable", username=username))

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


@main.route("/<username>/add_category", methods=["POST"])
@login_required
def add_category(username):
    """Add a category to the user's Apritable."""

    data = request.get_json()
    category_name = data.get("name", "").strip()

    if not category_name:
        return jsonify({"error": "No category name provided"}), 400

    existing = CustomCategory.query.filter_by(
        user_id=current_user.id,
        name=category_name,
    ).first()
    if existing:
        return jsonify({"error": "Category already exists"}), 400

    new_category = CustomCategory(user_id=current_user.id, name=category_name)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({"success": True, "name": category_name}), 200


@main.route("/<username>/add_pokemon", methods=["POST"])
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
        return redirect(url_for("apri.apritable", username=username))

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

    return redirect(url_for("apri.apritable", username=username) + "#add-pokemon-form")
