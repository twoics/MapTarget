"""
Module implementing the node of k-d tree
"""

# Local application imports
from .point import Point


class Node:
    """
    Class implementing the Node of k-d tree
    """

    def __init__(self, init_point: Point, data=None):
        self._point = init_point
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
