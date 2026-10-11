import ctypes
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import core_i18n


class CoreI18nTests(unittest.TestCase):
    def setUp(self):
        core_i18n._library = None
        self.native_library = Mock()
        self.native_library.core_i18n_gettext.return_value = b"Abbrechen"
        self.native_library.core_i18n_set_localedir.return_value = None
        self.library_patcher = patch.object(
            core_i18n.ctypes.util, "find_library", return_value="libcore-i18n.so"
        )
        self.find_library = self.library_patcher.start()
        self.addCleanup(self.library_patcher.stop)
        self.cdll_patcher = patch.object(
            core_i18n.ctypes, "CDLL", return_value=self.native_library
        )
        self.load_library = self.cdll_patcher.start()
        self.addCleanup(self.cdll_patcher.stop)
        self.addCleanup(setattr, core_i18n, "_library", None)

    def test_gettext_calls_system_library(self):
        self.assertEqual(core_i18n.gettext("Cancel"), "Abbrechen")
        self.find_library.assert_called_once_with("core-i18n")
        self.load_library.assert_called_once_with("libcore-i18n.so")
        self.native_library.core_i18n_gettext.assert_called_once_with(b"Cancel")
        self.assertEqual(
            self.native_library.core_i18n_gettext.argtypes, [ctypes.c_char_p]
        )
        self.assertIs(
            self.native_library.core_i18n_gettext.restype, ctypes.c_char_p
        )

    def test_set_localedir_calls_system_library(self):
        core_i18n.set_localedir(Path("/usr/share/locale"))
        self.native_library.core_i18n_set_localedir.assert_called_once_with(
            b"/usr/share/locale"
        )

    def test_c_api_aliases_match_python_functions(self):
        self.assertIs(core_i18n.core_i18n_gettext, core_i18n.gettext)
        self.assertIs(core_i18n.core_i18n_set_localedir, core_i18n.set_localedir)

    def test_missing_system_library_has_actionable_error(self):
        self.find_library.return_value = None
        with self.assertRaisesRegex(ImportError, "Install the system core-i18n"):
            core_i18n.gettext("Cancel")

    def test_library_is_loaded_only_once(self):
        core_i18n.gettext("Cancel")
        core_i18n.gettext("Save")
        self.find_library.assert_called_once_with("core-i18n")
        self.load_library.assert_called_once_with("libcore-i18n.so")


if __name__ == "__main__":
    unittest.main()
