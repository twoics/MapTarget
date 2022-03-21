from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5 import QtCore
from src.main.python.map.map_generator import Map
import io

EMPTY_AREA_WARNING = "Before searching for objects, you must first select the search area"
NULL_POINTS = """
Before searching for the closest point to the marker,
you must first select the search area, and the type of object
"""
EMPTY_MARKER = "Marker not found"


def _js_handler(js_string: str) -> tuple:
    """
    Returns the tuple obtained by processing the string
    :param js_string: JS string to be processed
    :return: Tuple from processed JS string
    """
    result = []
    split_str = js_string.replace("LatLng", "/").split("/")
    for item in split_str:
        item = item[:-1].replace('(', '').replace(')', '') \
            if item[-1] == ',' else item.replace('(', '').replace(')', '')

        if item != 'rectangle' and item != 'marker':
            item = tuple(map(float, item.split(',')))
        result.append(item)
    return tuple(result)


class WebEnginePage(QWebEnginePage):
    item_drawn = QtCore.pyqtSignal(tuple)
    zoom_changed = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def javaScriptAlert(self, QUrl, p_str):
        self.item_drawn.emit(_js_handler(p_str))

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        if level == 0:
            self.zoom_changed.emit(int(msg))


class MapUI(QtCore.QObject):
    """
    The class represents the UI for the map
    """
    some_error = QtCore.pyqtSignal(str)
    search_done = QtCore.pyqtSignal()
    refresh_map = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.marker_points = None
        self.rect_points = None
        self.mapa = None

        self.generator = Map()
        self.view = QWebEngineView()
        self.page = WebEnginePage(self.view)
        self.view.setPage(self.page)
        self._init_signals()

    def get_view(self):
        return self.view

    def find_nearest(self) -> None:
        """
        Finds the nearest object in the constructed map
        to the pivot, marks it with a special color, and updates the map
        :return: None
        """
        if self.marker_points is None:
            self.some_error.emit(EMPTY_MARKER)
            return

        result = self.generator.find_closest(self.marker_points)
        if result is None:
            self.some_error.emit(NULL_POINTS)
            return

        self.mapa = result
        self.refresh_map.emit()

    def set_map_by_query(self, query: str) -> None:
        """
        Builds a map by finding special objects by reserved type in the selected area
        :param query: Reserved type by which to find objects
        :return: None
        """
        
        if self.rect_points is None:
            self.search_done.emit()
            self.some_error.emit(EMPTY_AREA_WARNING)
            return

        if query in self.generator.get_reserved_queries():
            self.mapa = self.generator.map_by_reserved(query, self.rect_points[0], self.rect_points[2])
        else:
            self.mapa = self.generator.map_by_name(query, self.rect_points[0], self.rect_points[2])

        self.refresh_map.emit()

        self.search_done.emit()

    def clear_map(self) -> None:
        """
        Completely clear the map and parameters
        :return: None
        """
        self.mapa = self.generator.pure_map()
        self.refresh_map.emit()

    def _item_drawn(self, data: tuple) -> None:
        """
        Reads coordinates from a marker or map area
        :param data: The tuple of the coordinate
        :return: None
        """
        if data[0] == 'rectangle':
            self.rect_points = data[1:]
            self.marker_points = None
        else:
            self.rect_points = None
            self.marker_points = data[1]

    def _init_signals(self) -> None:
        """
        Initializing signals
        :return: None
        """
        self.page.item_drawn.connect(self._item_drawn)
        self.refresh_map.connect(self._refresh_map)
        self.page.zoom_changed.connect(self.generator.set_zoom)

    def _refresh_map(self):
        """
        Updates the map UI, on the current map
        :return: None
        """
        self.marker_points = None
        self.rect_points = None

        data = io.BytesIO()
        self.mapa.save(data, close_file=False)
        self.view.setHtml(data.getvalue().decode())  # give html of folium map to webengine
