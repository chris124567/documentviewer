"""This file serves static content such as robots.txt.

Mostly just for testing.
"""
from flask import Blueprint, current_app, request, send_from_directory

STATIC_BLUEPRINT = Blueprint('static', __name__)


@STATIC_BLUEPRINT.route('/robots.txt')
def static_from_root():
    """Serve {app.static_folder}/robots.txt."""
    return send_from_directory(current_app.static_folder, request.path[1:])
