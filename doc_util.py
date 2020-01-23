# doc_util.py
from sqlalchemy import desc
from flask import Markup, current_app
from app import db
from models import File


def search_documents(search, n):
    if (search == "" or search == None):  # if query is empty
        results = File.query.order_by(desc(
            File.id)).limit(n).all()  # return first n results
    else:  # search for query and return first n results
        results = File.query.filter(File.title.contains(search)).order_by(
            desc(File.id)).limit(n).all()
    return display_file_results(results)


def display_file_results(
        results
):  # generate html to be displayed on home and search pages: displays file name and title
    html = "<ol class=\"list-group\">"
    for file in results:
        html += "<li class=\"list-group-item\"><a href=\"/document/%d\">%s</a> <small class=\"text-muted\">%s</small></li>" % (file.id, file.title, file.description)
    html += "</ol>"
    return Markup(html)
