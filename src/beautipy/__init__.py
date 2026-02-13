"""BeautiPy: prettify data structures into human-readable strings."""

from importlib.metadata import PackageNotFoundError, version

from beautipy.core import beautify

__all__ = ["beautify", "__version__"]

try:
    __version__ = version("beautipy")
except PackageNotFoundError:
    __version__ = "0.1.0"
