# Standard library import
import sys

# Third party imports
from PyQt5 import QtCore

# Local application imports
from src.main.python.ui.map_ui import MapUI
from src.main.python.ui.main_ui import MainUI
from src.main.python.logic.map_generator import Map
from src.main.python.controller.controller import Controller
from src.main.python.base import BASE_CONTEXT


class Main:
    """A class that gathers the main components of the application into one"""

    def __init__(self):
        """
        Initializing main components
        """
        self._map_ui = MapUI()
        self._ui = MainUI(self._map_ui)
        self._map = Map()
        self._controller = Controller(self._map, self._map_ui)

        self._thread = QtCore.QThread()
        self._controller.moveToThread(self._thread)

        self._thread.start()
        self._ui.show()


if __name__ == "__main__":
    main = Main()
    exit_code = BASE_CONTEXT.app.exec()
    sys.exit(exit_code)
