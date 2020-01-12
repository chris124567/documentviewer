from flask import Blueprint, render_template, current_app, send_file
from . import db
from .models import File, User, login_required
from .doc_util import display_file_results
profile = Blueprint('profile', __name__)


@profile.route("/user/<userid>")
@login_required()
def user_profile(userid):
    user = User.query.get(userid)
    selected_file = File.query.filter_by(submitter=userid).all(
    )  # get all files uploaded by submitter with user id userid
    return render_template(
        "profile.html",
        name=user.name,
        results=display_file_results(selected_file))
