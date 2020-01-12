from flask import Blueprint, current_app, send_file, redirect, url_for
from . import db
from .models import File
from itsdangerous import TimedJSONWebSignatureSerializer

download = Blueprint('download', __name__)


@download.route("/download/<token>")
def download_doc(token):  #obfuscate download url
    s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
    try:
        docid = s.loads(token)[
            'docid']  # decrypt token and get document id from it
    except:
        return redirect(url_for(
            'main.index'))  # if we cant decrypt token redirect to home page

    selected_file = File.query.get(docid)
    return send_file(
        selected_file.file_path,
        attachment_filename=selected_file.original_name,
        as_attachment=True)
