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
    """The language QGIS shows its own interface in, such as "pt_BR": the
    translation it loaded (Settings > Options > General, or the system's
    language). QgsApplication.locale() is not used: without the override
    it gives only the language ("pt")."""
    name = ""
    app = QgsApplication.instance()
    try:
        name = app.translation() if app is not None else ""
    except AttributeError:
        pass
    if not name or name == "C":
        # QGIS stores the language it starts with here, also without the
        # override (for plugins).
        name = QgsSettings().value("locale/userLocale", "", type=str)
    return name or QLocale().name()


def candidates(name):
    """Translation files for locale `name`, best first: its own (pt_BR),
    its language's (pt), then another country's of that language (pt_PT
    for a plain "pt")."""
    name = name.replace("-", "_")
    language = name.split("_")[0]
    files = [FOLDER / f"{PREFIX}{name}.qm", FOLDER / f"{PREFIX}{language}.qm"]
    files += sorted(FOLDER.glob(f"{PREFIX}{language}_*.qm"))
    return [path for path in dict.fromkeys(files) if path.is_file()]


def install():
    """Load the translation for QGIS's language, if there is one."""
    global _translator  # pylint: disable=global-statement
    if _translator is not None:
        return
    for path in candidates(locale()):
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
