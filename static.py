from flask import Blueprint, current_app, request, send_from_directory

static = Blueprint('static', __name__)


# statically serve robots.txt
@static.route('/robots.txt')
def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])
