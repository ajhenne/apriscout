"""Flask route handles."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from sqlalchemy import func

from apriscout.utils import is_valid_username

from . import db
from .models import User

main = Blueprint("main", __name__)


@main.route("/")
def home():
    """Render the homepage."""
    return render_template("home.html")


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
            return redirect(url_for("main.user_page", username=user.username))

        flash("Invalid credentials.")

    return render_template("login.html")


@main.route("/logout")
@login_required
def logout():
    """Logout the currently authenticated user."""
    logout_user()
    return redirect(url_for("main.home"))


@main.route("/<username>")
def user_page(username):
    """Render the profile page for a given username."""
    user = User.query.filter(func.lower(User.username) == username.lower()).first()
    if user:
        return render_template("user.html", user=user)

    flash("User not found.")
    return redirect(url_for("main.home"))


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
        return redirect(url_for("main.user_page", username=user.username))

    flash("Username not found.")
    return redirect(request.referrer or url_for("main.home"))
