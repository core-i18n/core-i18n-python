# core-i18n-python

Python implementation of [core-i18n](https://github.com/core-i18n/core-i18n),
the standard dictionary of pre-translated UI strings.

## Install

```sh
python -m pip install core-i18n
```

## Usage

```python
from core_i18n import gettext

print(gettext("Cancel"))
```

The current language is selected using the standard gettext environment
variables (`LANGUAGE`, `LC_ALL`, `LC_MESSAGES`, and `LANG`). Unknown messages
and unavailable translations are returned unchanged. The bundled catalogs
cover the languages provided by the upstream library.

To load catalogs from another directory instead, set
`CORE_I18N_LOCALEDIR=/path/to/locale` or call `set_localedir()`:

```python
from core_i18n import gettext, set_localedir

set_localedir("/path/to/locale")
print(gettext("Cancel"))
```

`core_i18n_gettext` and `core_i18n_set_localedir` are also available as
names matching the C library API. Call `set_localedir(None)` to restore the
bundled catalogs (or the environment override).