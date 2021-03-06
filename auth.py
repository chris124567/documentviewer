# auth.py
"""This file handles login and signup (via POST requests), along with logout
functionality for users."""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from models import User, login_required
from app import APP_DATABASE

AUTH_BLUEPRINT = Blueprint('auth', __name__)


@AUTH_BLUEPRINT.route('/login')
def login():
    """This function loads the signin page."""
    return render_template('login.html')


@AUTH_BLUEPRINT.route('/login', methods=['POST'])
def login_post():
    """This assesses the validity of a users login credentials and allows them
    in if they are valid."""
    username = request.form.get('username')
    password = request.form.get('password')
    remember = (request.form.get('remember') == "on")

    # try to find user with specified email
    user = User.query.filter_by(username=username).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed
    # password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(
            url_for('auth.login')
        )  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right
    # credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))


@AUTH_BLUEPRINT.route('/signup')
def signup():
    """This function loads the signup page."""
    return render_template('signup.html')


@AUTH_BLUEPRINT.route('/signup', methods=['POST'])
def signup_post():
    """This function handles the database end of signing up.

    It hashes the passwor provided.  It also checks if the user already
    exists before registering.
    """
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first(
    )  # if this returns a user, then the username already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Username already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext
    # version isn't saved.
    new_user = User(
        username=username,
        name=name,
        password=generate_password_hash(password, method='sha256'),
        urole="regularuser")

    # add the new user to the database
    APP_DATABASE.session.add(new_user)
    APP_DATABASE.session.commit()
    flash("Welcome %s (%s)" % (username, name))
    return redirect(url_for('auth.login'))


@AUTH_BLUEPRINT.route('/logout')
@login_required()
def logout():
    """This function signs out a logged in user."""
    logout_user()
    return redirect(url_for('main.index'))
