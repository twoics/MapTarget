from abc import ABC, abstractmethod
from typing import Union
import folium
from src.main.python.logic.point import Point


class IMap(ABC):

    @abstractmethod
    def update_current_zoom(self, zoom: int) -> None:
        """
        Set zoom value
        This value is used when reloading
        the map to display the correct zoom
        :param zoom: Zoom value
        :return: None
        """
        pass

    @abstractmethod
    def pure_map(self) -> folium.Map:
        """
        Generate new Pure Map
        :return: Folium Map
        """
        pass

    @abstractmethod
    def find_objects(self, query: str, start_point: Point, end_point: Point) -> folium.Map:
        """
        Returns the map, with the found objects from the query,
        bounded by coordinates start_point, end_point
        :param query: Query to find objects
        :param start_point: Lower left limit of the search
        :param end_point: Right upper limit of the search
        :return: Map with points
        """
        pass

    @abstractmethod
    def nearest_object(self, pivot: Point) -> Union[folium.Map, None]:
        """
        Returns the map, with the marked object nearest to the point,
        if there are no objects on the map, returns None
        :param pivot: Point for which to look for the nearest object
        :return: Map if the nearest object is found, otherwise None
        """
        pass
