# models.py
from functools import wraps
from flask import redirect, url_for, current_app
from flask_login import UserMixin, current_user
from . import db


def login_required(role="ANY"): # role based authenticaton
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('main.index'))
            if ((current_user.urole != role) and (role != "ANY")):
                return redirect(url_for('main.index'))
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    name = db.Column(db.String(128))
    password = db.Column(db.String(256))
    urole = db.Column(db.String(64))

    def __init__(self, username, name, password, urole):
        self.username = username
        self.name = name
        self.password = password
        self.urole = urole

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_urole(self):
        return self.urole


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    original_name = db.Column(db.String(256))
    description = db.Column(db.String(512))
    file_path = db.Column(db.String(128))  # path to submitted file
    # max possible mime length according to rfc
    file_mime = db.Column(db.String(255))
    file_hash = db.Column(db.String(40), unique=True)  # sha1 hash length
    submitter = db.Column(db.Integer)  # submitter user id
