# upload.py

import magic
import textract

from flask import Blueprint, flash, current_app, url_for, redirect, render_template, request, Markup
from flask_login import current_user
from . import db
from .util import get_sha1_digest
from .models import login_required, File

upload = Blueprint('upload', __name__)

mime = magic.Magic(mime=True)  # dont reinitiate library if we don't have to
APPROVED_FILETYPES = {
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.oasis.opendocument.text", "application/pdf",
    "application/rtf", "text/rtf",
    "application/vnd.ms-word.document.macroEnabled.12"
}


@upload.route("/upload", methods=['GET'])
@login_required()
def upload_file():
    return render_template("upload.html")


@upload.route("/upload", methods=['POST'])
@login_required()
def upload_file_post():
    if (request.files == []):
        flash("Please attach a file")
        return redirect(url_for('upload.upload_file'))
    file_content = request.files['file'].read()
    file_mime = mime.from_buffer(file_content)

    if file_mime not in APPROVED_FILETYPES:
        flash(
            "File format forbidden.  Try using one of the following: epub, rtf, pdf, doc, or docx"
        )
        return redirect(url_for('upload.upload_file'))

    title = request.form.get('title')
    description = request.form.get('description')
    file_hash = get_sha1_digest(file_content)
    original_name = request.files['file'].filename
    submitter = current_user.id

    file = File.query.filter_by(file_hash=file_hash).first()
    if (file):  # if a file of the same hash exists
        flash(
            Markup(
                "Duplicate file! This file can already be found at the link: <a href=\"http://%s/document/%d\">%s/document/%d</a>"
                % (current_app.config['WEBSITE_HOST'].lower(), file.id,
                   current_app.config['WEBSITE_HOST'].lower(), file.id)))
        return redirect(url_for('upload.upload_file'))
    else:
        if (title == ""):
            title = original_name

        save_location = ''.join(
            [current_app.config['UPLOAD_FOLDER'], "/", file_hash])
        with open(save_location, "wb+") as storage:
            storage.write(file_content)
        
        new_file = File(
            title=title,
            original_name=original_name,
            description=description,
            file_path=save_location,
            file_mime=file_mime,
            file_hash=file_hash,
            submitter=submitter)
        db.session.add(new_file)
        db.session.commit()
        flash("Success!  Want to upload another document?")
        return redirect(url_for('upload.upload_file'))
