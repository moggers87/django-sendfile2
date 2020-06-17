Getting Started
---------------

Installation
============

Install via pip:

.. code-block:: shell

    pip install django-sendfile2

And then add ``django_sendfile`` to ``INSTALLED_APPS`` in your settings module.

.. note::

    It is not strictly nessessary to have django_sendfile in
    ``INSTALLED_APPS``, but this may change in future.


You will need to have the following set in your settings module:

* ``SENDFILE_BACKEND`` - the dotted module notation of the backend you wish to use
* ``SENDFILE_ROOT`` - the directory you wish to serve files from

Additionally, you may need to set ``SENDFILE_URL`` . See the :doc:`backends`
documentation for more details.


Use In Views
============

Use the :py:func:`~django_sendfile.sendfile` function instead of the usual
``HttpResponse`` function:

.. code-block:: python

    from django_sendfile import sendfile

    @login_required
    def my_secret_view(request):
        return sendfile(request, "/opt/my_secret.txt", mimetype="text/plain")

Alternatively, if you prefer class based views something like this would be required:

.. code-block:: python

    from django_sendfile import sendfile

    class MySecretView(LoginRequiredMixin, View):
        def render_to_response(self, context):
            return sendfile
