# util.py
import hashlib


def get_sha1_digest(file_content):  #calculate sha1 digest of a string
    h = hashlib.sha1()
    h.update(file_content)
    return h.hexdigest()
