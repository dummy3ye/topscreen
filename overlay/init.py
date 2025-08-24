"""overlay package initializer relocated to `init.py` per user request.

This file contains minimal package documentation and exposes package
submodules so callers can `from overlay import actions` or use
`from overlay import *` via the shim.
"""

from . import actions, window  # re-export submodules

__all__ = ["actions", "window"]
