import hashlib
import os

from modules import constants


def save_to_uploads(file):
    data = file.read()
    filename = hashlib.sha256(data).hexdigest() + '.jpg'
    with open(
            os.path.join(constants.UPLOAD_PATH, filename), mode='wb'
    ) as upload_file:
        upload_file.write(data)
    return filename
