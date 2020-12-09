import hashlib


def checksum(file_path):
    """Return the SHA256 of a file"""

    sha256_object = hashlib.sha256()
    with open(file_path, "rb") as file:
        while file_chunk := file.read(8192):
            sha256_object.update(file_chunk)
    return sha256_object.hexdigest()
