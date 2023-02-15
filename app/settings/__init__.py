from .base import *

try:
    from .local import *
    DEBUG = True
except ImportError:
    try:
        from .production import *
        DEBUG = False
    except ImportError:
        DEBUG = True
