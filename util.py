# util.py
"""This file contains miscellaneous utilities."""
import hashlib


def get_sha1_digest(file_content):
    """Calculate sha1 digest of a string."""
    sha1_hash = hashlib.sha1()
    sha1_hash.update(file_content)
    return sha1_hash.hexdigest()
