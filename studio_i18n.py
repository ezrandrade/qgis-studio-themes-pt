"""Translations of the plugin's own texts (i18n/qgis_studio_themes_<locale>.qm).

Only what the plugin shows is translated: the settings window, the
ribbon's tab, group and button names, toolbar names and messages. Keys
(tab names saved in the settings, objectNames, setting values) stay in
English: callers translate a text where they show it, with tr().

The locale is QGIS's own (Settings > Options > General > Locale, or the
system's), read once when the plugin loads, as QGIS applies a changed
language only after a restart. English needs no file: without one, tr()
returns the text as it is.
"""
from pathlib import Path

from qgis.core import QgsApplication, QgsSettings
from qgis.PyQt.QtCore import QCoreApplication, QLocale, QTranslator

CONTEXT = "QgisStudioThemes"
FOLDER = Path(__file__).resolve().parent / "i18n"
PREFIX = "qgis_studio_themes_"

_translator = None


def tr(text, disambiguation=None):
    """`text` in QGIS's language. `disambiguation` tells apart a text
    used with two meanings (e.g. a toolbar's name and a ribbon group's)."""
    return QCoreApplication.translate(CONTEXT, text, disambiguation)


def translated(text, disambiguation=None):
    """`text` translated, or None when no translation is loaded for it."""
    result = tr(text, disambiguation)
    return result if result != text else None


def locale():
    """QGIS's locale, such as "pt_BR"."""
    name = ""
    try:
        name = QgsApplication.locale() or ""
    except AttributeError:
        pass
    if not name:
        settings = QgsSettings()
        if settings.value("locale/overrideFlag", False, type=bool):
            name = settings.value("locale/userLocale", "", type=str)
    return name or QLocale().name()


def install():
    """Load the translation for QGIS's locale (pt_BR, else pt), if any."""
    global _translator  # pylint: disable=global-statement
    if _translator is not None:
        return
    name = locale().replace("-", "_")
    for candidate in dict.fromkeys((name, name.split("_")[0])):
        path = FOLDER / f"{PREFIX}{candidate}.qm"
        if not path.is_file():
            continue
        translator = QTranslator()
        if translator.load(str(path)):
            QCoreApplication.installTranslator(translator)
            _translator = translator
            return


def uninstall():
    global _translator  # pylint: disable=global-statement
    if _translator is not None:
        QCoreApplication.removeTranslator(_translator)
        _translator = None
