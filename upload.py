# upload.py

import magic
import textract
from ast import literal_eval

from flask import Blueprint, flash, current_app, url_for, redirect, render_template, request, Markup
from flask_login import current_user
from mime_map import get_extension_from_mimetype
from app import db, q, create_app
from util import get_sha1_digest
from models import login_required, File

upload = Blueprint('upload', __name__)

mime = magic.Magic(
    mime=True
)  # prevents us from having to reinitiate library every time we call the upload function
APPROVED_FILETYPES = {  # pdf, doc, docx, odt, rtf, and all variants with macros
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.oasis.opendocument.text", "application/pdf",
    "application/rtf", "text/rtf", "application/epub+zip",
    "application/vnd.ms-word.document.macroEnabled.12"
}


@upload.route("/upload", methods=['GET'])
@login_required()
def upload_file():
    return render_template("upload.html")


@upload.route("/upload", methods=['POST'])
@login_required()
def upload_file_post():
    file_content = request.files['file'].read(
    )  # since request.files returns a file object we have to call read() to get its contents
    file_mime = mime.from_buffer(file_content)  # detect mimetype of file

    if file_mime not in APPROVED_FILETYPES:
        flash(
            "File format forbidden.  Try using one of the following: epub, rtf, pdf, odt, doc, or docx"
        )
        return redirect(
            url_for('upload.upload_file')
        )  # redirect back to upload page if filetype is not permitted

    # dont get further information unless filetype is approved: save processor cycles
    title = request.form.get('title')
    description = request.form.get('description')
    file_hash = get_sha1_digest(file_content)
    original_name = request.files['file'].filename
    submitter = current_user.id

    file = File.query.filter_by(file_hash=file_hash).first()
    if (file):  # if a file of the same hash exists
        flash(
            Markup(
                "Duplicate file! This file can already be found at the link: <a href=\"/document/%d\">%s/document/%d</a>"
                % (file.id,
                   current_app.config['WEBSITE_HOST'], file.id)))
        return redirect(url_for('upload.upload_file'))
    else:
        if (title == ""):
            title = original_name

        job = q.enqueue_call(func=add_file_to_database, args=(submitter, title, original_name, description, file_content, file_mime, file_hash,), result_ttl=-1)

        flash("Success!  We are currently processing your document, it will appear on your profile page shortly.  Want to upload another document?")
        return redirect(url_for('upload.upload_file'))

def add_file_to_database(submitter, title, original_name, description, file_content, file_mime, file_hash):
    app = create_app()
    with app.app_context():
        # save file to UPLOAD_FOLDER/file_hash
        save_location = ''.join(
            [app.config['UPLOAD_FOLDER'], "/", file_hash])
        with open(save_location, "wb+") as storage:
            storage.write(file_content)  #actually write the file

        text = textract.process(save_location, language='eng', extension=get_extension_from_mimetype(file_mime)).decode('utf-8')

        new_file = File(
            title=title,
            original_name=original_name,
            description=description,
            file_path=save_location,
            file_mime=file_mime,
            transcript=text,
            file_hash=file_hash,
            submitter=submitter)

        db.session.add(new_file)  #add to database
        db.session.commit()
        return new_file.id