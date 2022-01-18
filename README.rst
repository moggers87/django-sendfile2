=================
Django Sendfile 2
=================

.. image:: https://github.com/moggers87/django-sendfile2/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/moggers87/django-sendfile2/actions/workflows/tests.yml
.. image:: https://readthedocs.org/projects/django-sendfile2/badge/?version=latest
   :target: https://django-sendfile2.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. inclusion-marker-do-not-remove-start

This is a wrapper around web-server specific methods for sending files to web
clients.  This is useful when Django needs to check permissions associated
files, but does not want to serve the actual bytes of the file itself.  i.e. as
serving large files is not what Django is made for.

Note this should not be used for regular file serving (e.g. CSS etc), only for
cases where you need Django to do some work before serving the actual file.

- Download: https://pypi.org/project/django-sendfile2/
- Source: https://github.com/moggers87/django-sendfile2
- Documentation: https://django-sendfile2.readthedocs.io/

Supported Python Versions
=========================

Python 3.7, 3.8, 3.9, and 3.10 are currently supported by this library.

Supported Django Versions
=========================

Django 2.2, 3.2, and 4.0 are currently supported by this library.

Fork
====

This project is a fork of `django-sendfile
<https://github.com/johnsensible/django-sendfile>`_. The original project
appears mostly dead and has a number of outstanding bugs (especially with
Python 3).

Funding
=======

If you have found django-sendfile2 to be useful and would like to see its continued
development, please consider `buying me a coffee
<https://ko-fi.com/moggers87>`_.

.. inclusion-marker-do-not-remove-end
