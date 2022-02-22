"""
Module implementing the node of k-d tree
"""

from .point import Point
from typing import Tuple

POINT = Tuple[float, float]


class Node:
    """
    Class implementing the Node of k-d tree
    """

    def __init__(self, init_point: POINT, data=None):
        if len(init_point) != 2:
            raise ValueError("The point must have 2 axes - x and y")
        self._point = Point(init_point[0], init_point[1])
        self._left_child = None
        self._right_child = None
        self._data = data

    def __str__(self):
        return f"Node - {self._point}"

    @property
    def left_child(self):
        return self._left_child

    @left_child.setter
    def left_child(self, node):
        self._left_child = node

    @property
    def right_child(self):
        return self._right_child

    @right_child.setter
    def right_child(self, node):
        self._right_child = node

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, point: Point):
        self._point = point

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
