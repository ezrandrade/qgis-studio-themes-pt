"""What differs between QGIS 3.44+ (Qt 5) and QGIS 4 (Qt 6), in one place.

QGIS 4 registers UI themes through QgsApplication.applicationThemeRegistry()
and announces a changed theme with QgsApplication.themeChanged. QGIS 3
has neither: it lists the folders in the user themes folder (where the
plugin builds its themes anyway) and applies a theme without a signal,
so ThemeWatcher notices the change instead. The Qt 5 differences are
small API ones (static methods that were instance methods, overloads Qt 5
lacks).
"""
from qgis.core import QgsApplication
from qgis.PyQt.QtCore import QEvent, QObject, QT_VERSION, QTimer
from qgis.PyQt.QtGui import QFontDatabase

QT6 = QT_VERSION >= 0x060000
# QGIS 4: themes are registered and themeChanged is emitted.
THEME_REGISTRY = hasattr(QgsApplication, "applicationThemeRegistry")

# Without themeChanged: how often the theme shown is checked, besides the
# check after every application-wide style change.
POLL_INTERVAL = 1500


def font_families():
    """The installed font families (a static method only from Qt 6)."""
    return QFontDatabase.families() if QT6 else QFontDatabase().families()


def register_theme(name, path):
    """Make a UI theme known to QGIS. QGIS 3 finds the folders in the user
    themes folder by itself (QgsApplication.uiThemes)."""
    if THEME_REGISTRY:
        QgsApplication.applicationThemeRegistry().addTheme(name, path)


def unregister_theme(name):
    if THEME_REGISTRY:
        QgsApplication.applicationThemeRegistry().removeTheme(name)


class ThemeWatcher(QObject):
    """Calls `callback` when the UI theme changes: QGIS 4's themeChanged,
    or on QGIS 3 (which applies a theme without a signal) a change of
    QgsApplication.themeName() seen after a style change of the main
    window (QGIS applies a theme with an application stylesheet) or at the
    latest after POLL_INTERVAL ms."""

    def __init__(self, callback, window=None):
        super().__init__()
        self._callback = callback
        self._window = window
        self._timer = None
        self._seen = None
        self._connected = False

    def start(self):
        if self._connected:
            return
        self._connected = True
        if THEME_REGISTRY:
            QgsApplication.instance().themeChanged.connect(self._callback)
            return
        self._seen = QgsApplication.themeName()
        if self._window is not None:
            self._window.installEventFilter(self)
        self._timer = QTimer(self)
        self._timer.setInterval(POLL_INTERVAL)
        self._timer.timeout.connect(self.check)
        self._timer.start()

    def stop(self):
        if not self._connected:
            return
        self._connected = False
        if THEME_REGISTRY:
            QgsApplication.instance().themeChanged.disconnect(self._callback)
            return
        if self._window is not None:
            self._window.removeEventFilter(self)
        if self._timer is not None:
            self._timer.stop()
            self._timer = None

    def check(self):
        """Call back if the theme shown changed since the last check."""
        theme = QgsApplication.themeName()
        if theme != self._seen:
            self._seen = theme
            self._callback()

    def eventFilter(self, watched, event):  # pylint: disable=invalid-name
        if event.type() == QEvent.Type.StyleChange:
            # After QGIS has set the theme's name (setUITheme sets it after
            # the stylesheet).
            QTimer.singleShot(0, self.check)
        return False
