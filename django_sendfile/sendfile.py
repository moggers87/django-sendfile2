from importlib import import_module
from mimetypes import guess_type
import os.path
import unicodedata

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.utils.encoding import force_str
from django.utils.http import urlquote


def _lazy_load(fn):
    _cached = []

    def _decorated():
        if not _cached:
            _cached.append(fn())
        return _cached[0]

    def clear():
        while _cached:
            _cached.pop()

    _decorated.clear = clear
    return _decorated


@_lazy_load
def _get_sendfile():
    backend = getattr(settings, 'SENDFILE_BACKEND', None)
    if not backend:
        raise ImproperlyConfigured('You ust specify a value for SENDFILE_BACKEND')
    module = import_module(backend)
    return module.sendfile


def sendfile(request, filename, attachment=False, attachment_filename=None,
             mimetype=None, encoding=None):
    '''
    create a response to send file using backend configured in SENDFILE_BACKEND

    Filename is the absolute path to the file to send.

    If attachment is True the content-disposition header will be set accordingly.
    This will typically prompt the user to download the file, rather
    than view it. But even if False, the user may still be prompted, depending
    on the browser capabilities and configuration.

    The content-disposition filename depends on the value of attachment_filename:

        None (default): Same as filename
        False: No content-disposition filename
        String: Value used as filename

    If no mimetype or encoding are specified, then they will be guessed via the
    filename (using the standard python mimetypes module)
    '''
    _sendfile = _get_sendfile()

    if not os.path.exists(filename):
        raise Http404('"%s" does not exist' % filename)

    guessed_mimetype, guessed_encoding = guess_type(filename)
    if mimetype is None:
        if guessed_mimetype:
            mimetype = guessed_mimetype
        else:
            mimetype = 'application/octet-stream'

    response = _sendfile(request, filename, mimetype=mimetype)

    # Suggest to view (inline) or download (attachment) the file
    parts = ['attachment' if attachment else 'inline']

    if attachment_filename is None:
        attachment_filename = os.path.basename(filename)

    if attachment_filename:
        attachment_filename = force_str(attachment_filename)
        ascii_filename = unicodedata.normalize('NFKD', attachment_filename)
        ascii_filename = ascii_filename.encode('ascii', 'ignore').decode()
        parts.append('filename="%s"' % ascii_filename)

        if ascii_filename != attachment_filename:
            quoted_filename = urlquote(attachment_filename)
            parts.append('filename*=UTF-8\'\'%s' % quoted_filename)

    response['Content-Disposition'] = '; '.join(parts)

    response['Content-length'] = os.path.getsize(filename)
    response['Content-Type'] = mimetype

    if not encoding:
        encoding = guessed_encoding
    if encoding:
        response['Content-Encoding'] = encoding

    return response
