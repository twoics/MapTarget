"""
This module provides communication between the UI and the logic
"""
# Third party imports
from PyQt5 import QtCore

# Local application imports
from ..logic.map_interface import IMap
from ..ui.view_interface import IView
from ..logic.point import Point


class Controller(QtCore.QObject):
    def __init__(self, mapa: IMap, view: IView):
        """
        The controller class that
        links the UI and the application logic
        :param mapa: Logic interface, through which the controller work the Map(Logic)
        :param view: UI interface, through which the controller work the UI
        """
        super().__init__()
        self._map = mapa
        self._view = view

        self.init_slots()
        self.pure_map()

    @QtCore.pyqtSlot()
    def pure_map(self) -> None:
        """
        Sets a clean, new map in the UI
        :return: None
        """
        new_map = self._map.pure_map()
        self._view.set_map(new_map)

    @QtCore.pyqtSlot(str, tuple, tuple)
    def all_objects_map(self, query: str, start_point: tuple, end_point: tuple):
        """
        Marks the objects on the map,
        got from the query, with the limit of coordinates
        :param query: Query by which to search for objects on the map (cafe, cinema, or the name of the object)
        :param start_point: Starting point of the search
        :param end_point: Ending point of the search
        :return: None
        """
        start = Point(start_point[0], start_point[1])
        end = Point(end_point[0], end_point[1])
        new_map = self._map.find_objects(query, start, end)
        self._view.set_map(new_map)

    @QtCore.pyqtSlot(tuple)
    def nearest_object_map(self, point: tuple):
        """
        Highlight the nearest object
        on the map nearest to the plotted point
        :param point: The point (lat, log) to which need to find the nearest object
        :return: None
        """
        pivot = Point(point[0], point[1])
        new_map = self._map.nearest_object(pivot)
        self._view.set_map(new_map)

    @QtCore.pyqtSlot(int)
    def zoom_changed(self, value: int) -> None:
        """
        Updates the zoom value in the map class
        :param value: The zoom value
        :return: None
        """
        self._map.update_current_zoom(value)

    def init_slots(self) -> None:
        """
        Initializing slots of signals
        :return: None
        """
        all_objects_request = self._view.all_object_request()
        nearest_object_request = self._view.nearest_object_request()
        pure_map_request = self._view.clear_map_request()
        zoom_changed = self._view.zoom_changed_signal()

        all_objects_request.connect(self.all_objects_map)
        nearest_object_request.connect(self.nearest_object_map)
        pure_map_request.connect(self.pure_map)
        zoom_changed.connect(self.zoom_changed)
