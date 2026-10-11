import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core_i18n import (
    core_i18n_gettext,
    gettext,
    set_localedir,
)


class GettextTests(unittest.TestCase):
    def setUp(self):
        set_localedir(None)

    def tearDown(self):
        set_localedir(None)

    def test_uses_bundled_catalog_for_current_language(self):
        with patch.dict(os.environ, {"LANGUAGE": "de"}, clear=True):
            self.assertEqual(gettext("Cancel"), "Abbrechen")

    def test_returns_unknown_message_unchanged(self):
        with patch.dict(os.environ, {"LANGUAGE": "de"}, clear=True):
            self.assertEqual(gettext("Not in the catalog"), "Not in the catalog")

    def test_environment_can_override_catalog_directory(self):
        catalog = Path(__file__).parents[1] / "core_i18n/locale/de/LC_MESSAGES/core-i18n.mo"
        with tempfile.TemporaryDirectory() as localedir:
            target = Path(localedir) / "de/LC_MESSAGES/core-i18n.mo"
            target.parent.mkdir(parents=True)
            shutil.copyfile(catalog, target)
            with patch.dict(
                os.environ,
                {"LANGUAGE": "de", "CORE_I18N_LOCALEDIR": localedir},
                clear=True,
            ):
                self.assertEqual(gettext("Cancel"), "Abbrechen")

    def test_explicit_localedir_and_c_api_alias(self):
        catalog = Path(__file__).parents[1] / "core_i18n/locale/de/LC_MESSAGES/core-i18n.mo"
        with tempfile.TemporaryDirectory() as localedir:
            target = Path(localedir) / "fr/LC_MESSAGES/core-i18n.mo"
            target.parent.mkdir(parents=True)
            shutil.copyfile(catalog, target)
            with patch.dict(os.environ, {"LANGUAGE": "fr"}, clear=True):
                set_localedir(localedir)
                self.assertEqual(core_i18n_gettext("Cancel"), "Abbrechen")


if __name__ == "__main__":
    unittest.main()
