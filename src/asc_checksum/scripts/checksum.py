import hashlib
import os


def _digest_file(path, hash_object):
    with open(path, "rb") as file:
        while file_chunk := file.read(8192):
            hash_object.update(file_chunk)


def _digest(path, hash_object):
    if os.path.isdir(path):
        for file_name in os.listdir(path):
            _digest(f"{path}/{file_name}", hash_object)
    else:
        _digest_file(path, hash_object)


def checksum(path):
    """Return the SHA256 of a file or a directory's content"""

    sha256_object = hashlib.sha256()
    _digest(path, sha256_object)
    return sha256_object.hexdigest()
