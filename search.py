from flask import Blueprint, render_template, request
from .doc_util import search_documents

search = Blueprint('search', __name__)


@search.route("/search")
def search_page():
    query = request.args.get('q')
    return render_template(
        "search.html", query=query, query_results=search_documents(query, 25)
    )  # we return 25 results for every query to prevent database overusage
