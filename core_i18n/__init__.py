import ctypes
import ctypes.util
import os
from typing import Optional, Union

_library = None


def _get_library():
    global _library
    if _library is None:
        library_name = ctypes.util.find_library("core-i18n")
        if library_name is None:
            raise ImportError(
                "The core-i18n shared library was not found. "
                "Install the system core-i18n library before using this package."
            )
        try:
            _library = ctypes.CDLL(library_name)
        except OSError as error:
            raise ImportError(
                "The core-i18n shared library could not be loaded."
            ) from error

        _library.core_i18n_gettext.argtypes = [ctypes.c_char_p]
        _library.core_i18n_gettext.restype = ctypes.c_char_p
        _library.core_i18n_set_localedir.argtypes = [ctypes.c_char_p]
        _library.core_i18n_set_localedir.restype = None
    return _library


def gettext(message: str) -> str:
    """Translate a message using the system core-i18n library."""
    translated = _get_library().core_i18n_gettext(message.encode("utf-8"))
    return translated.decode("utf-8")


def set_localedir(directory: Optional[Union[str, os.PathLike]] = None) -> None:
    """Set the locale catalog directory through the system core-i18n library."""
    path = os.fsencode(directory) if directory is not None else None
    _get_library().core_i18n_set_localedir(path)


core_i18n_gettext = gettext
core_i18n_set_localedir = set_localedir

__all__ = [
    "gettext",
    "set_localedir",
    "core_i18n_gettext",
    "core_i18n_set_localedir",
]
