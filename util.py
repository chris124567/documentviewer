# util.py
import hashlib


def get_sha1_digest(file_content):
    h = hashlib.sha1()
    h.update(file_content)
    return h.hexdigest()
