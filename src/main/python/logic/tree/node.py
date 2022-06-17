"""
Module implementing the node of k-d tree
"""

# Local application imports
from ..point import Point


class Node:
    """
    Class implementing the Node of k-d tree
    """

    def __init__(self, init_point: Point, data=None):
        """
        Initializing a KD tree node
        :param init_point: The point where the tree node is located
        :param data: Some date which is in the node
        """
        self._point = init_point
        self._left_child = None
        self._right_child = None
        self._data = data

    def __str__(self):
        return f"Node - {self._point}"

    @property
    def left_child(self):
        """
        Get left child from current node
        :return: Left child Node
        """
        return self._left_child

    @left_child.setter
    def left_child(self, node):
        """
        Set left child node from the current node
        :param node: Node to set
        :return: None
        """
        self._left_child = node

    @property
    def right_child(self):
        """
        Get right child from current node
        :return: Right child node
        """
        return self._right_child

    @right_child.setter
    def right_child(self, node):
        """
        Set right child node from the current node
        :param node: Node to set
        :return: None
        """
        self._right_child = node

    @property
    def point(self):
        """
        Get node point
        :return: Point where node located
        """
        return self._point

    @point.setter
    def point(self, point: Point):
        """
        Set point to the node
        :param point: Point object
        :return: None
        """
        self._point = point

    @property
    def data(self):
        """
        Get data from point
        :return: Point data
        """
        return self._data

    @data.setter
    def data(self, value):
        """
        Set data to node
        :param value: Some data
        :return: None
        """
        self._data = value
