# main.py
"""This file displays the index page."""
from flask import Blueprint, render_template
from doc_util import search_documents

MAIN_BLUEPRINT = Blueprint('main', __name__)


@MAIN_BLUEPRINT.route('/')
def index():
    """Shows the index page.

    It shows the newest 10 documents.
    """
    return render_template(
        'index.html', new_documents=search_documents(
            "", 10))  # return newest 10 documents on home page
