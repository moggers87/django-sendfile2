Changelog
---------

0.7.1
=====

:release-date: 2024-02-17

- Drop Python 3.7 support
- Drop Django 3.2 and 4.0 support
- Add Python 3.11 and 3.12 support
- Add Django 4.2 and 5.0 support

0.7.0
=====

:release-date: 2022-08-08

- Fix reflected file download vulnerability
- Add support for spaces in filenames

0.6.1
=====

:release-date: 2021-01-18

- Fixed Django 4.0 compatibility
- Add support for Python 3.10
- Remove support for Python 3.5 and 3.6
- Remove support for Django 3.1

0.6.0
=====

:release-date: 2020-06-17

- Fixed issue where django-sendfile could serve *any* file, even if it was
  outside ``SENDFILE_ROOT``. ``SENDFILE_ROOT`` is now required for all
  backends.

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
