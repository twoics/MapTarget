from ..logic.map_interface import IMap
from ..ui.view_interface import IView
from ..logic.point import Point
from PyQt5 import QtCore


class Controller(QtCore.QObject):
    def __init__(self, mapa: IMap, view: IView):
        super().__init__()
        self._map = mapa
        self._view = view

        self.init_slots()
        self.pure_map()

    @QtCore.pyqtSlot()
    def pure_map(self) -> None:
        new_map = self._map.pure_map()
        self._view.set_map(new_map)

    @QtCore.pyqtSlot(str, tuple, tuple)
    def all_objects_map(self, query: str, start_point: tuple, end_point: tuple):
        start = Point(start_point[0], start_point[1])
        end = Point(end_point[0], end_point[1])
        new_map = self._map.find_objects(query, start, end)
        self._view.set_map(new_map)

    @QtCore.pyqtSlot(tuple)
    def nearest_object_map(self, point: tuple):
        pivot = Point(point[0], point[1])
        new_map = self._map.nearest_object(pivot)
        self._view.set_map(new_map)

    @QtCore.pyqtSlot(int)
    def zoom_changed(self, value: int) -> None:
        self._map.update_current_zoom(value)

    def init_slots(self) -> None:
        all_objects_request = self._view.all_object_request()
        nearest_object_request = self._view.nearest_object_request()
        pure_map_request = self._view.clear_map_request()
        zoom_changed = self._view.zoom_changed_signal()

        all_objects_request.connect(self.all_objects_map)
        nearest_object_request.connect(self.nearest_object_map)
        pure_map_request.connect(self.pure_map)
        zoom_changed.connect(self.zoom_changed)
