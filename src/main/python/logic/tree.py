"""
Module implementing the k-d tree
"""

# TODO Write Test for build K-D tree and for Closest Distance

# TODO Operation add
# TODO Operation del
# TODO Operation in area

from math import sqrt
from typing import Union
from .point import Point
from .node import Node


class KdTree:
    """
    The class that implements KD tree
    """

    def __init__(self, init_points: list):
        """
        Builds a k-d tree based on the set of points passed in the array
        :param init_points: Points on which to build a k-d tree
        """
        self._space = 2  # Since this tree was built for the map, the space is two-dimensional
        self._root_node = self._build_tree(init_points)

    def __str__(self):
        self._print_tree(self._root_node)

    def get_root(self) -> Node:
        """
        :return: Root Node of KD tree
        """
        return self._root_node

    def rebuild_tree(self, points_list: list) -> Union[Node, None]:
        """
        Rebuild KD tree by points
        :param points_list: List with points by which to build a tree
        :return: Root Node of KD-tree
        """
        self._root_node = self._build_tree(points_list)
        return self._root_node

    def closest_point(self, point: Point) -> Union[Point, None]:
        """
        Looks for the closest point of the tree next to the pivot
        :param point: Pivot point
        :return: Nearest Point
        """
        return self._closest_point(self._root_node, point)

    def _print_tree(self, node: Node, level=0) -> None:
        """
        Printed k-d tree
        :param node: Node for print
        :param level: Recursion level
        :return: None
        """
        if node is not None:
            self._print_tree(node.left_child, level + 1)
            print(' ' * 15 * level + '->', node.point)
            self._print_tree(node.right_child, level + 1)

    def _closest_point(self, root: Node, point: Point, depth=0) -> Union[Point, None]:
        """
        Calculate the closest point to pivot
        :param root: Root node of K-d tree
        :param point: The point to which we are looking for the closest
        :param depth: Recursive parameter
        :return: Closest Point
        """
        if root is None:
            return None

        axis = depth % self._space

        if point[axis] < root.point[axis]:
            next_branch = root.left_child
            opposite_branch = root.right_child
        else:
            next_branch = root.right_child
            opposite_branch = root.left_child

        best = _nearest_point(point,
                              self._closest_point(next_branch,
                                                  point,
                                                  depth + 1),
                              root.point)

        # If distance from pivot to 'best' node bigger than module by distance(perpendicular)
        # from pivot to space section -> check opposite branch (maybe there is a node closer)
        if _euclidean_distance(point, best) > abs(point[axis] - root.point[axis]):
            best = _nearest_point(point,
                                  self._closest_point(opposite_branch,
                                                      point,
                                                      depth + 1),
                                  best)

        return best

    def _build_tree(self, points_list: list, depth=0, parent: Node = None) -> Union[Node, None]:
        """
        Builds a k-d tree
        :param points_list: The list of points from which to build the tree
        :param depth: Recursive parameter
        :param parent: Recursive parameter
        :return:
        """
        length = len(points_list)

        if length <= 0:
            return None

        axis = depth % self._space

        # Sort point by axis (by 'x' or 'y' )
        sorted_points = [point for point in sorted(points_list, key=lambda point: point[axis])]

        root = Node(sorted_points[length // 2])

        # Left part
        self._build_tree(sorted_points[:length // 2], depth + 1, root)
        # Right part
        self._build_tree(sorted_points[length // 2 + 1:], depth + 1, root)

        # The parent node has a opposite partition plane
        parent_axis = 1 - axis

        if parent is not None:
            if root.point[parent_axis] < parent.point[parent_axis]:
                parent.left_child = root
            else:
                parent.right_child = root

        return root


def _nearest_point(pivot: Point, point_1: Point, point_2: Point) -> Union[Point, None]:
    """
    Returns the point that is closer to the pivot
    :param pivot: The point to which we are looking for the closest
    :param point_1: First point
    :param point_2: Second point
    :return: Nearest point to pivot
    """
    if point_1 is None:
        return point_2

    if point_2 is None:
        return point_1

    distance_1 = _euclidean_distance(pivot, point_1)
    distance_2 = _euclidean_distance(pivot, point_2)

    if distance_1 < distance_2:
        return point_1
    else:
        return point_2


def _euclidean_distance(point_1: Point, point_2: Point) -> float:
    """
    Calculate euclidean distance by 2 points
    :param point_1: First point
    :param point_2: Second point
    :return: Euclidean distance
    """
    x1, y1 = point_1[0], point_1[1]
    x2, y2 = point_2[0], point_2[1]

    delta_x = x1 - x2
    delta_y = y1 - y2

    return sqrt(delta_x ** 2 + delta_y ** 2)
