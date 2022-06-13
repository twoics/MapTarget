from abc import ABC, abstractmethod
from PyQt5 import QtCore
import folium


class IView(ABC):

    @abstractmethod
    def zoom_changed_signal(self) -> QtCore.pyqtSignal(int):
        pass

    @abstractmethod
    def nearest_object_request(self) -> QtCore.pyqtSignal(tuple):
        pass

    @abstractmethod
    def all_object_request(self) -> QtCore.pyqtSignal(str, tuple, tuple):
        pass

    @abstractmethod
    def clear_map_request(self) -> QtCore.pyqtSignal():
        pass

    @abstractmethod
    def set_map(self, new_map: folium.Map) -> None:
        pass
