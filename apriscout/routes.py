"""Flask route handles."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func

from apriscout.constants import apriball_names
from apriscout.services import update_user_collection
from apriscout.utils import is_valid_username

from . import db
from .models import Pokemon, User, UserPokemon

main = Blueprint("main", __name__)


@main.route("/")
def home():
    """Render the homepage."""
    return render_template("home.html")


########################################################################################
# LOGIN FUNCTIONS


@main.route("/register", methods=["GET", "POST"])
def register():
    """Register a user through a form."""
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter(func.lower(User.username) == username.lower()).first():
            flash("Username already exists.")
            return redirect(url_for("main.register"))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Account created. Please login.")

        return redirect(url_for("main.login"))

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    """Login a user given username and password, if valid."""
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        user = User.query.filter(
            func.lower(User.username) == request.form["username"].lower(),
        ).first()

        if user and user.check_password(request.form["password"]):
            login_user(user, remember=True)
            return redirect(url_for("main.apritable", username=user.username))

        flash("Invalid credentials.")

    return render_template("login.html")


@main.route("/logout")
@login_required
def logout():
    """Logout the currently authenticated user."""
    logout_user()
    return redirect(url_for("main.home"))


########################################################################################
# APRITABLE FUNCTIONS


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
        return redirect(url_for("main.apritable", username=username))

    user_collection = UserPokemon.query.filter_by(user_id=user.id).join(Pokemon).all()
    all_pokemon = Pokemon.query.order_by(Pokemon.dex_num).all()

    return render_template(
        "apritable.html",
        user=user,
        can_edit=can_edit,
        collection=user_collection,
        all_pokemon=all_pokemon,
        ball_list=apriball_names,
    )


@main.route("/<username>/add_pokemon", methods=["POST"])
@login_required
def add_pokemon(username):
    """Add a Pokemon to the user's Apritable."""

    user = User.query.filter(func.lower(User.username) == username.lower()).first()
    if not user:
        flash("User not found.")
        return redirect(url_for("main.home"))

    if current_user.id != user.id:
        flash("You are not authorised to edit someone else's collection.")

    pokemon_id = request.form.get("pokemon_id")
    if not pokemon_id:
        flash("No pokemon selected.")
        return redirect(url_for("main.apritable", username=username))

    already_exists = UserPokemon.query.filter_by(
        user_id=user.id,
        pokemon_id=pokemon_id,
    ).first()
    if already_exists:
        flash("That Pokemon already exists in your collection.")
    else:
        new_entry = UserPokemon(user_id=user.id, pokemon_id=pokemon_id)
        db.session.add(new_entry)
        db.session.commit()
        flash(f"{Pokemon.query.get(pokemon_id).name} added to your collection!")

    return redirect(url_for("main.apritable", username=username))


@main.route("/search")
def search_user():
    """Search for a username and render their profile page."""
    search_user_query = request.args.get("search_user", "").strip()

    if not search_user_query or not is_valid_username:
        flash("Username not found.")
        return redirect(request.referrer or url_for("main.home"))

    user = User.query.filter(
        func.lower(User.username) == search_user_query.lower(),
    ).first()
    if user:
        return redirect(url_for("main.apritable", username=user.username))

    flash("Username not found.")
    return redirect(request.referrer or url_for("main.home"))
