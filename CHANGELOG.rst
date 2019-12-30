Changelog
---------


0.5.1
=====

:release-date: 2019-12-30

- Fix issue with versioneer not being updated about the package name change
   - tox now does a proper sdist and install to avoid this in future

0.5.0
=====

:release-date: 2019-12-30

- Rename Python package from ``sendfile`` to ``django_sendfile``

   - This will require changing ``SENDFILE_BACKEND``, ``INSTALLED_APPS``, and
     any imports

- Remove code used to support Python 2.7
- Add support for the latest versions of Django and Python

Earlier Releases
================

Sorry, we didn't keep a changelog prior to version 0.5.0!
