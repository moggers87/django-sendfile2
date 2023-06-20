from . import _version
from .utils import sendfile  # noqa

__version__ = _version.get_versions()['version']

# old versions of django-sendfile have this, so keep it for compatibility
VERSION = tuple(__version__.split("+")[0].split("."))
