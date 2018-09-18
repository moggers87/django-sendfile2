try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import versioneer


setup(
    name='django-sendfile2',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Abstraction to offload file uploads to web-server (e.g. Apache with mod_xsendfile) once Django has checked permissions etc.',
    long_description=open('README.rst').read(),
    author='Matt Molyneaux',
    author_email='moggers87+git@moggers87.co.uk',
    url='https://github.com/moggers87/django-sendfile2',
    license='BSD',

    install_requires=['django', 'six'],
    packages=['sendfile', 'sendfile.backends'],
    package_dir={
        'sendfile': 'sendfile',
        'sendfile.backends': 'sendfile/backends',
    },
    package_data={
        'sendfile': ['testfile.txt'],
    },

    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
