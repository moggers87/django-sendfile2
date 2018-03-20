from django.http import HttpResponse
import six


def sendfile(request, filename, **kwargs):
    filename = six.text_type(filename)
    if six.PY2:
        filename = filename.encode("utf-8")

    response = HttpResponse()
    response['X-Sendfile'] = filename

    return response
