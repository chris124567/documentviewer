# upload.py
"""This file allows us to upload files.

We restrict the upload mimetypes.
"""
import magic
import textract

from flask import Blueprint, flash, current_app, url_for, redirect, render_template, request, Markup
from flask_login import current_user
from mime_map import get_extension_from_mimetype
from app import APP_DATABASE
from util import get_sha1_digest
from models import login_required, File

UPLOAD_BLUEPRINT = Blueprint('upload', __name__)

MIME = magic.Magic(
    mime=True
)  # prevents us from having to reinitiate library every time we call the upload function

APPROVED_FILETYPES = {  # pdf, doc, docx, odt, rtf, and all variants with macros
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.oasis.opendocument.text", "application/pdf",
    "application/rtf", "text/rtf", "application/epub+zip",
    "application/vnd.ms-word.document.macroEnabled.12"
}


@UPLOAD_BLUEPRINT.route("/upload", methods=['GET'])
@login_required()
def upload_file():
    """This loads the upload page.

    It contains a form for the file itself, a title, and a description.
    If a title is not supplied, the original file name is used as a
    title.
    """
    return render_template("upload.html")


@UPLOAD_BLUEPRINT.route("/upload", methods=['POST'])
@login_required()
def upload_file_post():
    """This makes sure a file:

    1) has an approved mime-type 2) does not already exist (checks hash)
    3) has a title (uses original title if one not supplied) And then
    saves it to the database File column.
    """
    file_content = request.files['file'].read(
    )  # since request.files returns a file object we have to call read() to get its contents
    file_mime = MIME.from_buffer(file_content)  # detect mimetype of file

    if file_mime not in APPROVED_FILETYPES:
        flash(
            "File format forbidden.  Try using one of the following: epub, rtf, pdf, odt, doc, or \
docx"
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
    if file:  # if a file of the same hash exists
        flash(
            Markup(
                "Duplicate file! This file can already be found at the link: <a href=\"/document/%\
d\">%s/document/%d</a>"
                % (file.id, current_app.config['WEBSITE_HOST'], file.id)))
        return redirect(url_for('upload.upload_file'))

    if title == "":
        title = original_name

    add_file_to_database(submitter, title, original_name, description,
                         file_content, file_mime, file_hash)

    flash(
        "Success!  We are currently processing your document, it will appear on your profile page \
shortly.  Want to upload another document?"
    )
    return redirect(url_for('upload.upload_file'))


def add_file_to_database(submitter, title, original_name, description,
                         file_content, file_mime, file_hash):
    """
    This:
    1) Writes a file to the disk ({UPLOAD_FOLDER}/hash),
    2) Attempts to generate a transcript of the file,
    3) Saves the file to the database.
    """
    # save file to UPLOAD_FOLDER/file_hash
    save_location = ''.join(
        [current_app.config['UPLOAD_FOLDER'], "/", file_hash])
    with open(save_location, "wb+") as storage:
        storage.write(file_content)  # actually write the file

    try:
        text = textract.process(
            save_location,
            language='eng',
            extension=get_extension_from_mimetype(file_mime)).decode(
                'utf-8')
    except (textract.exceptions.UnknownMethod, textract.exceptions.ShellError):
        text = ""

    new_file = File(
        title=title,
        original_name=original_name,
        description=description,
        file_path=save_location,
        file_mime=file_mime,
        transcript=text,
        file_hash=file_hash,
        submitter=submitter)

    APP_DATABASE.session.add(new_file)  # add to database
    APP_DATABASE.session.commit()
    return new_file.id
