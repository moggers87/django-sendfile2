Custom Backend
--------------

A django-sendfile2 backend is simply a Python module that contains a callable
named ``sendfile``, for example:

.. code-block:: python
    :caption: myModule.py

    def sendfile(request, filename, **kwargs):
        response = HttpResponse()
        response["X-My-Custom-Header"] = filename
        return response

Assuming the module is in your Python path and named ``myModule``, you'd set ``SENDILE_BACKEND`` like so:

.. code-block:: python
    :caption: settings.py

    SENDFILE_BACKEND = "myModule"

…and use django-sendfile2 in your views as you would normally.

.. warning::

    Don't get confused between this ``sendfile`` callable and
    :py:func:`django_sendfile.sendfile`. The latter accepts slightly different
    arguments and takes care of various ``Content-*`` headers.
