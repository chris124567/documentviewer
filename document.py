# document.py
"""This file generates a temporary download URL for a given document ID.

This helps prevent mirroring of the website.
"""

from flask import Blueprint, current_app, render_template
from itsdangerous import TimedJSONWebSignatureSerializer
from models import File

DOCUMENT_BLUEPRINT = Blueprint('document', __name__)


@DOCUMENT_BLUEPRINT.route("/document/<docid>")
def document_view(
        docid):
    """This function obfuscates download url and prevents easy mirroring of
    site."""
    encrypted = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'],
                                                60 * 30)  # 60 secs by 30 mins
    token = encrypted.dumps({'docid': docid}).decode('utf-8')  # encode user id
    doc = File.query.get(docid)
    return render_template(
        "document.html",
        token=token,
        doc_name=doc.title,
        transcript=doc.transcript)
