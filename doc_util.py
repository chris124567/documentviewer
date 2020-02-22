# doc_util.py
"""This file contains utilities for searching for documents via SQL and
formatting the HTML to display the results."""
from sqlalchemy import desc
from flask import Markup
from models import File


def search_documents(search, num_results):
    """Searches for n documents with a given query for title using SQL and
    returns the HTML formatted results."""
    if (search is None or search in ""):  # if query is empty
        results = File.query.order_by(desc(
            File.id)).limit(num_results).all()  # return first n results
    else:  # search for query and return first n results
        results = File.query.filter(File.title.contains(search)).order_by(
            desc(File.id)).limit(num_results).all()
    return display_file_results(results)


def display_file_results(results):
    """Generates the HTML to be displayed on home and search pages (displays
    file name, title, and description)."""
    html = "<ol class=\"list-group\">"
    for file in results:
        html += "<li class=\"list-group-item\"><a href=\"/document/%d\">%s</a> <small class=\"text\
-muted\">%s</small></li>" % (
            file.id, file.title, file.description)
    html += "</ol>"
    return Markup(html)
