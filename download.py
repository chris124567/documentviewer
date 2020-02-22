# download.py
"""This file decrypts the temporary download URL for every file.

This help prevent mirroring of the website.
"""
from flask import Blueprint, current_app, send_file, redirect, flash, url_for
import itsdangerous
from models import File

DOWNLOAD_BLUEPRINT = Blueprint('download', __name__)


@DOWNLOAD_BLUEPRINT.route("/download/<token>")
def download_doc(token):
    """This function decrypts the encrypted URL's generated in document.py and
    then sends the file of the given document ID."""
    encrypted = itsdangerous.TimedJSONWebSignatureSerializer(
        current_app.config['SECRET_KEY'])
    try:
        docid = encrypted.loads(token)[
            'docid']  # decrypt token and get document id from it
    except itsdangerous.BadData:
        flash("Unable to find given document")
        redirect(url_for('main.index'))

    selected_file = File.query.get(docid)
    return send_file(
        selected_file.file_path,
        attachment_filename=selected_file.original_name,
        as_attachment=True,
        mimetype=selected_file.file_mime)
