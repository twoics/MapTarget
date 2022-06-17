# Standard library import
import sys

# Third party imports
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

# Local application imports
from python.ui.map_ui import MapUI
from python.ui.main_ui import MainUI
from python.logic.map_generator import Map
from python.controller.controller import Controller


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
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
