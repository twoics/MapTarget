"""
Module implementing the 2-dimension point
This module uses a lot of other modules, so it was taken out
"""
# Standard library import
import math


class Point:
    """
    Class implementing the Point of Node location
    """

    def __init__(self, x: float = None, y: float = None):
        self._x = x
        self._y = y

    def __str__(self):
        return f"({self._x}, {self._y})"

    def __getitem__(self, item):
        if item == 0:
            return self._x
        elif item == 1:
            return self._y
        raise Exception("Only 0 or 1 expected")

    def __eq__(self, other):
        if not isinstance(other, Point):
            raise TypeError("Objects to be compared with Point must be of type Point")
        # TODO FIX THIS

        if other.x == self._x and other.y == self._y:
            return True
        return False

    def euclidean_distance(self, point) -> float:
        """
        Calculates the Euclidean distance between two points
        :param point: Other point
        :return: Euclidean distance
        """
        if not isinstance(point, Point):
            raise TypeError("point must be of type Point")

        delta_x = self.x - point.x
        delta_y = self._y - point.y
        return math.sqrt(delta_x ** 2 + delta_y ** 2)

    def middle_point(self, other_point):
        """
        Find middle between current and other point
        :param other_point: Other point
        :return: Middle Point
        """
        if not isinstance(other_point, Point):
            raise TypeError("other_point must be of type Point")

        return Point((other_point.x + self.x) / 2, (other_point.y + self.y) / 2)

    @property
    def points(self) -> tuple:
        """
        Get tuple coordinates (x, y)
        :return: Tuple with coordinates
        """
        return self._x, self._y

    @property
    def x(self) -> float:
        """
        :return: Get x coordinate
        """
        return self._x

    @x.setter
    def x(self, new_x: float):
        """
        Set x coordinate
        :param new_x: Value to set
        :return: None
        """
        self._x = new_x

    @property
    def y(self) -> float:
        """
        :return: Get y coordinate
        """
        return self._y

    @y.setter
    def y(self, new_y: float):
        """
        Set y coordinate
        :param new_y: Value to set
        :return: None
        """
        self._y = new_y
