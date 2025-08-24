"""Package initializer for the `overlay` package.

This module intentionally avoids importing heavy GUI dependencies at import
time. `actions` is small and safe to import; `window` (which imports PyQt5)
is lazy-loaded when accessed.
"""
from importlib import import_module
from types import ModuleType
from typing import Any

from . import actions  # safe, lightweight

__all__ = ["actions", "window"]


def __getattr__(name: str) -> Any:  # lazy-load window to avoid PyQt5 import on simple imports
	if name == "window":
		mod = import_module(".window", __package__)
		globals()["window"] = mod
		return mod
	raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
	return sorted(list(globals().keys()) + __all__)
"""overlay package for topscreen

Contains GUI window and adb action helpers.
"""

__all__ = ["actions", "window"]
