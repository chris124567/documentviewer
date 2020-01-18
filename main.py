# main.py

from flask import Blueprint, render_template
from html import unescape
from flask_login import login_required, current_user
from .doc_util import search_documents
main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template(
        'index.html', new_documents=search_documents(
            "", 10))  # return newest 10 documents on home page
