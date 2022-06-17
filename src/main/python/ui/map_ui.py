"""
The module is used to display the map
"""

# Standard library import
import io
from typing import Union

# Third party imports
import folium
from PyQt5 import QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Local application imports
from .view_interface import IView
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

    # Signal that is sent to the main UI to show an error message
    # Param: Message error
    some_error = QtCore.pyqtSignal(str)

    # The signal that is emitted when the map is finished is sent to stop gif
    search_done = QtCore.pyqtSignal()

    # New clear map setting signal
    pure_map_signal = QtCore.pyqtSignal()

    # Signal to set the map and mark the nearest object
    # Param: point - (latitude, longitude)
    find_closest_signal = QtCore.pyqtSignal(tuple)

    # Signal, to set the map and mark all objects satisfying the query
    # Param: (query, start_point, end_point)
    find_objects_signal = QtCore.pyqtSignal(str, tuple, tuple)

    # Internal signal, used to update the map
    refresh_map = QtCore.pyqtSignal()

    def __init__(self):
        """
        Initializing the folium map visualization
        """
        super().__init__()
        self._marker_point = None
        self._rect_points = None
        self._mapa = None

        self._view = QWebEngineView()
        self._page = WebEnginePage(self._view)

        self._view.setPage(self._page)
        self._init_signals()

    def zoom_changed_signal(self) -> QtCore.pyqtSignal(int):
        """
        param: Zoom value
        :return: Signal for listening, emitted when user zooms in/out the map
        """
        return self._page.zoom_changed

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

    def set_map(self, new_map: Union[folium.Map, None]):
        """
        Displays the transferred map
        :param new_map: Map to set
        :return: None
        """
        self.search_done.emit()
        if new_map is None:
            self._emit_error("None points on map")
            return

        self._mapa = new_map
        self.refresh_map.emit()

    def get_view(self):
        """
        :return: Get QWebEngineView
        """
        return self._view

    @QtCore.pyqtSlot()
    def request_nearest_object(self) -> None:
        """
        Request for the closest object to a point
        :return: None
        """
        if self._marker_point is None:
            self._emit_error(self.EMPTY_MARKER)
            return
        self.find_closest_signal.emit(self._marker_point)

    @QtCore.pyqtSlot(str)
    def request_objects(self, query: str):
        """
        Request to find objects on query in the selected area
        :param query: Query by which to search for objects
        :return: None
        """
        if self._rect_points is None:
            self._emit_error(self.EMPTY_AREA)
            return
        self.find_objects_signal.emit(query, self._rect_points[0], self._rect_points[2])

    @QtCore.pyqtSlot()
    def request_pure_map(self):
        """
        Request to install a blank map
        :return: None
        """
        self.pure_map_signal.emit()

    @QtCore.pyqtSlot(tuple)
    def _item_drawn(self, data: tuple) -> None:
        """
        Reads coordinates from a marker or map area
        :param data: The tuple of the coordinate
        :return: None
        """
        if data[0] == 'rectangle':
            self._rect_points = data[1:]
            self._marker_point = None
        else:
            self._rect_points = None
            self._marker_point = data[1]

    @QtCore.pyqtSlot()
    def _refresh_map(self):
        """
        Updates the map UI, on the current map
        :return: None
        """
        self._marker_point = None
        self._rect_points = None

        data = io.BytesIO()
        self._mapa.save(data, close_file=False)

        # give html of folium map to webengine
        self._view.setHtml(data.getvalue().decode())

    def _emit_error(self, message: str):
        """
        Sends a signal with an error message to the main UI
        :param message: Error message
        :return: None
        """
        self.some_error.emit(message)
        self.search_done.emit()

    def _init_signals(self) -> None:
        """
        Initializing signals
        :return: None
        """
        self._page.item_drawn.connect(self._item_drawn)
        self.refresh_map.connect(self._refresh_map)
