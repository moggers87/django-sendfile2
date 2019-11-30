from urllib.parse import quote
import os.path

from django.conf import settings


def _convert_file_to_url(filename):
    relpath = os.path.relpath(filename, settings.SENDFILE_ROOT)

    url = [settings.SENDFILE_URL]

    while relpath:
        relpath, head = os.path.split(relpath)
        url.insert(1, head)

    return quote('/'.join(url))
