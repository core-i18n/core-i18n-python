import gettext as _gettext
import os
from pathlib import Path
from typing import Optional, Union

_DOMAIN = "core-i18n"
_BUNDLED_LOCALEDIR = Path(__file__).parent / "locale"
_localedir: Optional[str] = None


def set_localedir(directory: Optional[Union[str, os.PathLike]] = None) -> None:
    """Set the directory containing gettext catalogs, or reset to the default."""
    global _localedir
    _localedir = os.fspath(directory) if directory is not None else None


def gettext(message: str) -> str:
    """Translate a message for the current locale, returning it unchanged if absent."""
    localedir = _localedir
    if localedir is None:
        localedir = os.environ.get("CORE_I18N_LOCALEDIR") or str(_BUNDLED_LOCALEDIR)
    translation = _gettext.translation(_DOMAIN, localedir=localedir, fallback=True)
    return translation.gettext(message)


core_i18n_gettext = gettext
core_i18n_set_localedir = set_localedir

__all__ = [
    "gettext",
    "set_localedir",
    "core_i18n_gettext",
    "core_i18n_set_localedir",
]
