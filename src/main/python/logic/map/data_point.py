"""
A module that implements a class that is used to
contain information about an object:
location point and information
"""

# Third party imports
from ..point import Point


class DataPoint:
    def __init__(self, point: Point, data: dict):
        """
        Initializing an object to hold information about object
        :param point: The point on the map where the object is located
        :param data: Object information
        """
        self._point = point
        self._data = data

    @property
    def point(self) -> Point:
        """
        Get object point
        :return: The point on map where object is located
        """
        return self._point

    @property
    def data(self) -> dict:
        """
        Get object data
        :return: Data from object on map
        """
        return self._data

    @property
    def tuple_data(self) -> tuple:
        """
        Get all data from an object as a tuple
        :return: (point: Point, data: dict)
        """
        return self._point, self.data
