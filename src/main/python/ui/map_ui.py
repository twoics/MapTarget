"""
The module is used to display the map
"""

# Standard library import
import io

# Third party imports
import folium
from PyQt5 import QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Local application imports
from src.main.python.ui.view_interface import IView
from .web_engine import WebEnginePage


class WindowViewMeta(type(QtCore.QObject), type(IView)):
    pass


class MapUI(QtCore.QObject, IView, metaclass=WindowViewMeta):
    """
    The class represents the UI for the map
    Implement the interface through which the controller works with the ui card
    """

    EMPTY_AREA = "Before searching for objects, you must select the search area"
    EMPTY_MARKER = "Marker not found"

    some_error = QtCore.pyqtSignal(str)
    search_done = QtCore.pyqtSignal()
    refresh_map = QtCore.pyqtSignal()

    pure_map_signal = QtCore.pyqtSignal()
    find_closest_signal = QtCore.pyqtSignal(tuple)
    find_objects_signal = QtCore.pyqtSignal(str, tuple, tuple)

    def __init__(self):
        """
        Initializing the folium map visualization
        """
        super().__init__()
        self.marker_point = None
        self.rect_points = None
        self.mapa = None

        self.view = QWebEngineView()

        self.page = WebEnginePage(self.view)
        self.view.setPage(self.page)
        self._init_signals()

    def zoom_changed_signal(self) -> QtCore.pyqtSignal(int):
        """
        param: Zoom value
        :return: Signal for listening, emitted when user zooms in/out the map
        """
        return self.page.zoom_changed

    def nearest_object_request(self) -> QtCore.pyqtSignal(tuple):
        """
        param: Point coordinates
        :return: Signal for listening, emitted when the user wants to
        get the closest object, to the selected point
        """
        return self.find_closest_signal

    def all_object_request(self) -> QtCore.pyqtSignal(str, tuple, tuple):
        """
        param: query, start_point, end_point
        :return:Signal for listening, emitted when the user
        wants to get all objects in some area
        """
        return self.find_objects_signal

    def clear_map_request(self) -> QtCore.pyqtSignal():
        """
        :return: Signal for listening, emitted when the user wants to get a blank map
        """
        return self.pure_map_signal

    def set_map(self, new_map: folium.Map):
        """
        Displays the transferred map
        :param new_map: Map to set
        :return: None
        """
        self.mapa = new_map
        self.refresh_map.emit()

    def request_nearest_object(self) -> None:
        """
        Request for the closest object to a point
        :return: None
        """
        if self.marker_point is None:
            self.some_error.emit(self.EMPTY_MARKER)
            return
        self.find_closest_signal.emit(self.marker_point)

    def request_objects(self, query: str):
        """
        Request to find objects on query in the selected area
        :param query: Query by which to search for objects
        :return: None
        """
        if self.rect_points is None:
            self.search_done.emit()
            self.some_error.emit(self.EMPTY_AREA)
            return
        self.find_objects_signal.emit(query, self.rect_points[0], self.rect_points[2])

    def request_pure_map(self):
        """
        Request to install a blank map
        :return: None
        """
        self.pure_map_signal.emit()

    def get_view(self):
        """
        :return: Get QWebEngineView
        """
        return self.view

    def _item_drawn(self, data: tuple) -> None:
        """
        Reads coordinates from a marker or map area
        :param data: The tuple of the coordinate
        :return: None
        """
        if data[0] == 'rectangle':
            self.rect_points = data[1:]
            self.marker_point = None
        else:
            self.rect_points = None
            self.marker_point = data[1]

    def _init_signals(self) -> None:
        """
        Initializing signals
        :return: None
        """
        self.page.item_drawn.connect(self._item_drawn)
        self.refresh_map.connect(self._refresh_map)

    def _refresh_map(self):
        """
        Updates the map UI, on the current map
        :return: None
        """
        self.marker_point = None
        self.rect_points = None

        data = io.BytesIO()
        self.mapa.save(data, close_file=False)
        self.view.setHtml(data.getvalue().decode())  # give html of folium map to webengine
