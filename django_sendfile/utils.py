from functools import lru_cache
from importlib import import_module
from mimetypes import guess_type
from os.path import normpath
from pathlib import Path, PurePath
from urllib.parse import quote
import logging
import unicodedata

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404

logger = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def _get_sendfile():
    backend = getattr(settings, 'SENDFILE_BACKEND', None)
    if not backend:
        raise ImproperlyConfigured('You must specify a value for SENDFILE_BACKEND')
    module = import_module(backend)
    return module.sendfile


def _convert_file_to_url(path):
    try:
        url_root = PurePath(getattr(settings, "SENDFILE_URL", None))
    except TypeError:
        return path

    path_root = PurePath(settings.SENDFILE_ROOT)
    path_obj = PurePath(path)

    relpath = path_obj.relative_to(path_root)
    url = normpath(url_root / relpath)

    return quote(url)


def _sanitize_path(filepath):
    try:
        path_root = Path(getattr(settings, 'SENDFILE_ROOT', None))
    except TypeError:
        raise ImproperlyConfigured('You must specify a value for SENDFILE_ROOT')

    filepath_abs = Path(normpath(path_root / filepath))

    # if filepath_abs is not relative to path_root, relative_to throws an error
    try:
        filepath_abs.relative_to(path_root)
    except ValueError:
        raise Http404('{} wrt {} is impossible'.format(filepath_abs, path_root))

    return filepath_abs


def sendfile(request, filename, attachment=False, attachment_filename=None,
             mimetype=None, encoding=None):
    """
    Create a response to send file using backend configured in ``SENDFILE_BACKEND``

    ``filename`` is the absolute path to the file to send.

    If ``attachment`` is ``True`` the ``Content-Disposition`` header will be set accordingly.
    This will typically prompt the user to download the file, rather
    than view it. But even if ``False``, the user may still be prompted, depending
    on the browser capabilities and configuration.

    The ``Content-Disposition`` filename depends on the value of ``attachment_filename``:

        ``None`` (default): Same as ``filename``
        ``False``: No ``Content-Disposition`` filename
        ``String``: Value used as filename

    If neither ``mimetype`` or ``encoding`` are specified, then they will be guessed via the
    filename (using the standard Python mimetypes module)
    """
    filepath_obj = _sanitize_path(filename)
    logger.debug('filename \'%s\' requested "\
        "-> filepath \'%s\' obtained', filename, filepath_obj)
    _sendfile = _get_sendfile()

    if not filepath_obj.exists():
        raise Http404('"%s" does not exist' % filepath_obj)

    guessed_mimetype, guessed_encoding = guess_type(str(filepath_obj))
    if mimetype is None:
        if guessed_mimetype:
            mimetype = guessed_mimetype
        else:
            mimetype = 'application/octet-stream'

    response = _sendfile(request, filepath_obj, mimetype=mimetype)

    # Suggest to view (inline) or download (attachment) the file
    parts = ['attachment' if attachment else 'inline']

    if attachment_filename is None:
        attachment_filename = filepath_obj.name

    if attachment_filename:
        attachment_filename = str(attachment_filename).replace("\\", "\\\\").replace('"', r"\"")
        ascii_filename = unicodedata.normalize('NFKD', attachment_filename)
        ascii_filename = ascii_filename.encode('ascii', 'ignore').decode()
        parts.append('filename="%s"' % ascii_filename)

        if ascii_filename != attachment_filename:
            quoted_filename = quote(attachment_filename)
            parts.append('filename*=UTF-8\'\'%s' % quoted_filename)

    response['Content-Disposition'] = '; '.join(parts)

    response['Content-length'] = filepath_obj.stat().st_size
    response['Content-Type'] = mimetype

    if not encoding:
        encoding = guessed_encoding
    if encoding:
        response['Content-Encoding'] = encoding

    return response
