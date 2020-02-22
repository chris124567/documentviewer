# models.py
"""This file contains the SQLALCHEMY relational models for the user and file
tables.

It also contains a wrapper for role based authentication in Flask.
"""

from functools import wraps
from flask import redirect, url_for
from flask_login import UserMixin, current_user
from app import APP_DATABASE


def login_required(role="ANY"):  # role based authenticaton
    """This function allows for role-based authentication in Flask by comparing
    the current_user.urole with the required role for a given page."""
    def wrapper(function):
        @wraps(function)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('main.index'))
            if ((current_user.urole != role) and (role not in "ANY")):
                return redirect(url_for('main.index'))
            return function(*args, **kwargs)

        return decorated_view

    return wrapper


class User(UserMixin, APP_DATABASE.Model):  # pylint: disable=too-few-public-methods
    """This is the model for users.

    It contains their ID, username (128 max char string), real name (128 max char string), hashed
    password (64 chars - length of sha256 hash), and their role (64 max char string).
    """
    id = APP_DATABASE.Column(APP_DATABASE.Integer, primary_key=True)
    username = APP_DATABASE.Column(APP_DATABASE.String(128), unique=True)
    name = APP_DATABASE.Column(APP_DATABASE.String(128))
    password = APP_DATABASE.Column(APP_DATABASE.String(64))
    urole = APP_DATABASE.Column(APP_DATABASE.String(64))


class File(APP_DATABASE.Model):  # pylint: disable=too-few-public-methods
    """This is the model for uploaded files (documents).

    They have an ID, title, original file_name, description, file path,
    transcript of the text, submitter's user ID and hash to prevent
    duplicates.
    """
    id = APP_DATABASE.Column(APP_DATABASE.Integer, primary_key=True)
    title = APP_DATABASE.Column(APP_DATABASE.String(256))
    original_name = APP_DATABASE.Column(APP_DATABASE.String(256))
    description = APP_DATABASE.Column(APP_DATABASE.String(1024))
    file_path = APP_DATABASE.Column(
        APP_DATABASE.String(128))  # path to submitted file
    # max possible mime length according to rfc
    file_mime = APP_DATABASE.Column(APP_DATABASE.String(255))
    transcript = APP_DATABASE.Column(APP_DATABASE.Text)
    file_hash = APP_DATABASE.Column(
        APP_DATABASE.String(40), unique=True)  # sha1 hash length
    submitter = APP_DATABASE.Column(APP_DATABASE.Integer)  # submitter user id
