# core-i18n-python

Python bindings for the system
[core-i18n](https://github.com/core-i18n/core-i18n) C library.

## Requirements

```sh
python -m pip install core-i18n-python
```

Install the core-i18n C library and its language catalogs separately using
your operating system's package manager. This Python package does not bundle
translation catalogs.

## Usage

```python
from core_i18n import gettext

print(gettext("Cancel"))
```

The system library selects the current language and returns unknown messages
unchanged.

To override the system library's locale catalog directory, call
`set_localedir()`:

```python
from core_i18n import gettext, set_localedir

set_localedir("/path/to/locale")
print(gettext("Cancel"))
```

`core_i18n_gettext` and `core_i18n_set_localedir` are also available as names
matching the C library API. The shared library is loaded lazily when either
function is first called.