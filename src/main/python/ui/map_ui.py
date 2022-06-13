import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5 import QtCore
import io
from src.main.python.ui.view_interface import IView

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


class WindowViewMeta(type(QtCore.QObject), type(IView)):
    pass


class MapUI(QtCore.QObject, IView, metaclass=WindowViewMeta):
    """
    The class represents the UI for the map
    """

    some_error = QtCore.pyqtSignal(str)
    search_done = QtCore.pyqtSignal()
    refresh_map = QtCore.pyqtSignal()

    pure_map_signal = QtCore.pyqtSignal()
    find_closest_signal = QtCore.pyqtSignal(tuple)
    find_objects_signal = QtCore.pyqtSignal(str, tuple, tuple)

    def __init__(self):
        super().__init__()
        self.marker_point = None
        self.rect_points = None
        self.mapa = None

        self.view = QWebEngineView()

        self.page = WebEnginePage(self.view)
        self.view.setPage(self.page)
        self._init_signals()

    def zoom_changed_signal(self) -> QtCore.pyqtSignal(int):
        return self.page.zoom_changed

    def nearest_object_request(self) -> QtCore.pyqtSignal(tuple):
        return self.find_closest_signal

    def all_object_request(self) -> QtCore.pyqtSignal(str, tuple, tuple):
        return self.find_objects_signal

    def clear_map_request(self) -> QtCore.pyqtSignal():
        return self.pure_map_signal

    def set_map(self, new_map: folium.Map):
        self.mapa = new_map
        self.refresh_map.emit()

    def request_nearest_object(self) -> None:
        if self.marker_point is None:
            self.some_error.emit(EMPTY_MARKER)
            return
        self.find_closest_signal.emit(self.marker_point)

    def request_objects(self, query: str):
        if self.rect_points is None:
            self.search_done.emit()
            self.some_error.emit(EMPTY_AREA_WARNING)
            return
        self.find_objects_signal.emit(query, self.rect_points[0], self.rect_points[2])

    def request_pure_map(self):
        self.pure_map_signal.emit()

    def get_view(self):
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
        # self.page.zoom_changed.connect(self.generator.set_zoom)

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
