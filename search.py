"""This file displays the search page."""
from flask import Blueprint, render_template, request, current_app
from doc_util import search_documents

SEARCH_BLUEPRINT = Blueprint('search', __name__)


@SEARCH_BLUEPRINT.route("/search")
def search_page():
    """Uses the query parameter ("q") to search the title column of the
    database for results."""
    query = request.args.get('q')
    return render_template(
        "search.html", query=query, query_results=search_documents(query, current_app.config['NUM_\
RESULTS'])
    )  # we return app.config['NUM_RESULTS'] results for every query to prevent database overusage
