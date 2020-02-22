"""This file dispalys a user's profile page."""

from sqlalchemy import desc
from flask import Blueprint, render_template, current_app
from models import File, User, login_required
from doc_util import display_file_results

PROFILE_BLUEPRINT = Blueprint('profile', __name__)


@PROFILE_BLUEPRINT.route("/user/<userid>")
@login_required()
def user_profile(userid):
    """This displays a users profile page.

    It shows their name and their uploaded files.
    """
    user = User.query.get(userid)
    selected_file = File.query.filter_by(submitter=userid).order_by(
        desc(File.id)).limit(current_app.config['NUM_RESULTS']).all()
    # get last NUM_RESULTS files uploaded by submitter with user id userid - prevent copying of site
    return render_template(
        "profile.html",
        name=user.name,
        results=display_file_results(selected_file))
