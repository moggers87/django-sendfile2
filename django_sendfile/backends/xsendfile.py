from django.http import HttpResponse


def sendfile(request, filename, **kwargs):
    response = HttpResponse()
    response['X-Sendfile'] = str(filename)

    return response
