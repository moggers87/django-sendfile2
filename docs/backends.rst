Backends
--------

Backends are specified by setting ``SENDFILE_BACKEND`` to the dotted path of
the backend you wish to use. E.g.:

.. code-block:: python
   :caption: settings.py

   SENDFILE_BACKEND = "django_sendfile.backends.simple"

Development backend
===================

:py:mod:`django_sendfile.backends.development`

The Development backend is only meant for use while writing code.  It uses
Django's static file serving code to do the job, which is only meant for
development.  It reads the whole file into memory and the sends it down the
wire - not good for big files, but OK when you are just testing things out.

It will work with the Django dev server and anywhere else you can run Django.

Simple backend
==============

:py:mod:`django_sendfile.backends.simple`

This backend is one step up from the development backend.  It uses Django's
``django.core.files.base.File`` class to try and stream files from disk.  However
some middleware (e.g. GzipMiddleware) that rewrites content will causes the
entire file to be loaded into memory.  So only use this backend if you are not
using middleware that rewrites content or you only have very small files.


mod_wsgi backend
================

:py:mod:`django_sendfile.backends.mod_wsgi`

The mod_wsgi backend will only work when using mod_wsgi in daemon mode, not in
embedded mode.  It requires a bit more work to get it to do the same job as
xsendfile though.  However some may find it easier to setup, as they don't need
to compile and install mod_xsendfile_.

Firstly there one more Django setting that needs to be given:

* ``SENDFILE_URL`` - internal URL prefix for all files served via sendfile

These settings are needed as this backend makes mod_wsgi_ send an internal
redirect, so we have to convert a file path into a URL.  This means that the
files are visible via Apache_ by default too.  So we need to get Apache_ to
hide those files from anything that's not an internal redirect.  To so this we
can use some mod_rewrite_ magic along these lines:

.. code-block:: apache

    RewriteEngine On
    # see if we're on an internal redirect or not
    RewriteCond %{THE_REQUEST} ^[\S]+\ /private/
    RewriteRule ^/private/ - [F]

    Alias /private/ /home/john/Development/myapp/private/
    <Directory /home/john/Development/myapp/private/>
        Order deny,allow
        Allow from all
    </Directory>


In this case I have also set:

.. code-block:: python
    :caption: settings.py

    SENDFILE_ROOT = '/home/john/Development/myapp/private/'
    SENDFILE_URL = '/private'


All files are stored in a folder called 'private'.  We forbid access to this
folder (``RewriteRule ^/private/ - [F]``) if someone tries to access it directly
(``RewriteCond %{THE_REQUEST} ^[\S]+\ /private/``) by checking the original
request (``THE_REQUEST``).

Allegedly ``IS_SUBREQ`` can be used to `perform the same job
<http://www.mail-archive.com/django-users@googlegroups.com/msg96718.html>`_,
but I was unable to get this working.


Nginx backend
=============

:py:mod:`django_sendfile.backends.nginx`

As with the mod_wsgi backend you need to set an extra settings:

* ``SENDFILE_URL`` - internal URL prefix for all files served via sendfile

You then need to configure Nginx to only allow internal access to the files you
wish to serve.  More details on this `are here
<https://www.nginx.com/resources/wiki/start/topics/examples/xsendfile/>`_.

For example though, if I use the Django settings:

.. code-block:: python
    :caption: settings.py

    SENDFILE_ROOT = '/home/john/Development/django-sendfile/examples/protected_downloads/protected'
    SENDFILE_URL = '/protected'

Then the matching location block in nginx.conf would be:

.. code-block:: nginx

    location /protected/ {
      internal;
      root   /home/john/Development/django-sendfile/examples/protected_downloads;
    }

You need to pay attention to whether you have trailing slashes or not on the
``SENDFILE_URL`` and ``SENDFILE_ROOT`` values, otherwise you may not get the
right URL being sent to Nginx and you may get 404s.  You should be able to see
what file Nginx is trying to load in the error.log if this happens.  From there
it should be fairly easy to work out what the right settings are.


xsendfile backend
=================

:py:mod:`django_sendfile.backends.xsendfile`

Install either mod_xsendfile_ in Apache_ or use Lighthttpd_.  You may need to
configure mod_xsendfile_, but that should be as simple as:

.. code-block:: lighty

    XSendFile On

In your virtualhost file/conf file.


.. _mod_xsendfile: https://tn123.org/mod_xsendfile/
.. _Apache: http://httpd.apache.org/
.. _Lighthttpd: http://www.lighttpd.net/
.. _mod_wsgi: http://www.modwsgi.org/
.. _mod_rewrite: http://httpd.apache.org/docs/current/mod/mod_rewrite.html

