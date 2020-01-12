# doc_util.py
from sqlalchemy import desc
from flask import Markup, current_app
from . import db
from .models import File


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
    html = ""
    i = 1
    for file in results:
        html += "%d. <a href=\"http://%s/document/%d\">%s</a>" % (
            i, current_app.config['WEBSITE_HOST'], file.id, file.title)
        html += "<br>"
        i += 1
    return Markup(html)
