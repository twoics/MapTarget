"""
The UI interface of the card, through
which the controller interacts with it
"""
# Standard library import
from abc import ABC, abstractmethod

# Third party imports
from PyQt5 import QtCore
import folium


class IView(ABC):

    @abstractmethod
    def zoom_changed_signal(self) -> QtCore.pyqtSignal(int):
        """
        param: Zoom value
        :return: Signal for listening, emitted when user zooms in/out the map
        """
        pass

    @abstractmethod
    def nearest_object_request(self) -> QtCore.pyqtSignal(tuple):
        """
        param: Point coordinates
        :return: Signal for listening, emitted when the user wants to
        get the closest object, to the selected point
        """
        pass

    @abstractmethod
    def all_object_request(self) -> QtCore.pyqtSignal(str, tuple, tuple):
        """
        param: query, start_point, end_point
        :return:Signal for listening, emitted when the user
        wants to get all objects in some area
        """
        pass

    @abstractmethod
    def clear_map_request(self) -> QtCore.pyqtSignal():
        """
        :return: Signal for listening, emitted when the user wants to get a blank map
        """
        pass

    @abstractmethod
    def set_map(self, new_map: folium.Map) -> None:
        """
        Displays the transferred map
        :param new_map: Map to set
        :return: None
        """
        pass
