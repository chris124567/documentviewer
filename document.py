# document.py
from flask import Blueprint, current_app, render_template
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer
from .models import File

document = Blueprint('document', __name__)


@document.route("/document/<docid>")
def document_view(
        docid):  # obfuscate download url and prevent easy mirroring of site
    s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'],
                                        60 * 30)  # 60 secs by 30 mins
    token = s.dumps({'docid': docid}).decode('utf-8')  # encode user id
    doc_name = File.query.get(docid).title
    return render_template("document.html", token=token, doc_name=doc_name)
