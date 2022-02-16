"""
Module implementing the k-d tree
"""

# TODO Write Test for build K-D tree and for Closest Distance

# TODO Operation add
# TODO Operation del
# TODO Operation in area

from math import sqrt
from typing import Union


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

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, new_x: float):
        self._x = new_x

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, new_y: float):
        self._y = new_y


class Node:
    """
    Class implementing the Node of k-d tree
    """

    def __init__(self, init_point: Point = None):
        self._point = init_point
        self._left_child = None
        self._right_child = None

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


class KdTree:
    def __init__(self):
        self._space = 2  # Since this tree was built for the map, the space is two-dimensional

    def print_tree(self, node: Node, level=0) -> None:
        if node is not None:
            self.print_tree(node.left_child, level + 1)
            print(' ' * 15 * level + '->', node.point)
            self.print_tree(node.right_child, level + 1)

    def build_kd_tree(self, points_list: list, depth=0, parent: Node = None) -> Union[Node, None]:
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
        self.build_kd_tree(sorted_points[:length // 2], depth + 1, root)
        # Right part
        self.build_kd_tree(sorted_points[length // 2 + 1:], depth + 1, root)

        # The parent node has a opposite partition plane
        parent_axis = 1 - axis

        if parent is not None:
            if root.point[parent_axis] < parent.point[parent_axis]:
                parent.left_child = root
            else:
                parent.right_child = root

        return root

    def kdtree_closest_point(self, root_kd_tree: Node, point: Point, depth=0) -> Union[Point, None]:
        """
        Calculate the closest point to pivot
        :param root_kd_tree: Root node of K-d tree
        :param point: The point to which we are looking for the closest
        :param depth: Recursive parameter
        :return: Closest Point
        """
        if root_kd_tree is None:
            return None

        axis = depth % self._space

        if point[axis] < root_kd_tree.point[axis]:
            next_branch = root_kd_tree.left_child
            opposite_branch = root_kd_tree.right_child
        else:
            next_branch = root_kd_tree.right_child
            opposite_branch = root_kd_tree.left_child

        best = _nearest_point(point,
                              self.kdtree_closest_point(next_branch,
                                                        point,
                                                        depth + 1),
                              root_kd_tree.point)

        # If distance from pivot to 'best' node bigger than module by distance(perpendicular)
        # from pivot to space section -> check opposite branch (maybe there is a node closer)
        if _euclidean_distance(point, best) > abs(point[axis] - root_kd_tree.point[axis]):
            best = _nearest_point(point,
                                  self.kdtree_closest_point(opposite_branch,
                                                            point,
                                                            depth + 1),
                                  best)

        return best


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
