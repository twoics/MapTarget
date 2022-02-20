"""
Module implementing the k-d tree
"""

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
        self._points_in_area = list()
        self._dimension = 2  # Since this tree was built for the map, the space is two-dimensional
        self._root_node = self._build_tree(init_points.copy())
        self._output_str = ""

    def __str__(self):
        self._output_str = ""
        self._tree_to_str(self._root_node)
        return self._output_str

    def get_root(self) -> Node:
        """
        :return: Root Node of KD tree
        """
        return self._root_node

    def add(self, point: Point) -> None:
        """
        Add node into the K-D tree
        :param point: Point to be added
        :return: None
        """
        if self._root_node:
            self._add(Node(point), self._root_node)
        else:
            self._root_node = Node(point)

    def remove(self, point: Point) -> None:
        """
        Delete Node from k-d Tree
        :param point: Point to delete
        :return: None
        """
        if point is None or self._root_node is None:
            return
        if self._root_node.left_child is None and self._root_node.right_child is None and point == \
                self._root_node.point:
            self._root_node = None
        else:
            self._del(Node(point), self._root_node)

    def check_entry(self, point_1: Point, point_2: Point) -> list:
        """
        Outputs a list of nodes that are included in the area from point1 to point2
        :param point_1: First point
        :param point_2: Second point
        :return: List with nodes
        """
        self._points_in_area.clear()
        if point_1.x > point_2.x or point_1.y > point_2.y:
            raise ValueError("First point must be less then second")
        self._entry_field(point_1, point_2, self._root_node)
        return self._points_in_area.copy()

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

    def _tree_to_str(self, node: Node, level=0) -> None:
        """
        Printed k-d tree
        :param node: Node for print
        :param level: Recursion level
        :return: None
        """
        if node is not None:
            self._tree_to_str(node.right_child, level + 1)
            self._output_str += (' ' * 8 * level + '->' + str(node.point) + "\n")
            self._tree_to_str(node.left_child, level + 1)

    def _entry_field(self, start_pos: Point, end_pos: Point, node: Node, depth=0) -> None:
        """
        Iterated by nodes, depending on their location, relative to the area, goes
        to the left or right subtree, otherwise if the area intersects the dimension of current node,
        checks if the node is in the area, then iterates through both subtrees
        :param start_pos: Start area position
        :param end_pos: End area position
        :param node: Current Node
        :param depth: Tree depth
        :return: None
        """
        if node is None:
            return None

        axis = depth % self._dimension
        point = node.point

        if point[axis] > start_pos[axis] and point[axis] > end_pos[axis]:  # Area left or down
            self._entry_field(start_pos, end_pos, node.left_child, depth + 1)
        elif point[axis] < start_pos[axis] and point[axis] < end_pos[axis]:  # Area right or up
            self._entry_field(start_pos, end_pos, node.right_child, depth + 1)
        else:  # Area across axis
            if start_pos.x <= point.x <= end_pos.x and start_pos.y <= point.y <= end_pos.y:  # Point in area
                self._points_in_area.append(node.point)
            self._entry_field(start_pos, end_pos, node.left_child, depth + 1)
            self._entry_field(start_pos, end_pos, node.right_child, depth + 1)

    def _add(self, node: Node, root: Node, depth=0) -> None:
        """
        Traverses the tree, looking for a place to insert a node, once found, inserts the node
        :param node: Node to be added
        :param root: Root node K-d tree
        :param depth: Recursive parameter
        :return: None
        """
        if root is None:
            return None

        axis = depth % self._dimension
        point = node.point

        if point[axis] < root.point[axis]:
            next_branch = root.left_child
            if next_branch is None:
                root.left_child = node
        else:
            next_branch = root.right_child
            if next_branch is None:
                root.right_child = node

        self._add(node, next_branch, depth + 1)

    def _del(self, del_node: Node, curr_root: Node, dimension: int = 0) -> Union[Node, None]:
        """
        Traverses the tree, looking node for delete, delete it
        :param del_node: Node to delete
        :param curr_root: Root Node
        :param dimension: Current dimension - x == 0, y == 1
        :return: None
        """

        if curr_root is None:
            return None

        dimension = dimension % self._dimension

        if del_node.point == curr_root.point:

            if curr_root.right_child is not None:
                right_min = self._minimum_node(curr_root.right_child, dimension, dimension + 1)
                curr_root.point = right_min.point
                curr_root.right_child = self._del(right_min, curr_root.right_child, dimension + 1)

            elif curr_root.left_child is not None:
                left_min = self._minimum_node(curr_root.left_child, dimension, dimension + 1)
                curr_root.point = left_min.point
                curr_root.right_child = self._del(left_min, curr_root.left_child, dimension + 1)
                curr_root.left_child = None

            else:
                return None

            return curr_root

        if del_node.point[dimension] < curr_root.point[dimension]:
            curr_root.left_child = self._del(del_node, curr_root.left_child, dimension + 1)

        else:
            curr_root.right_child = self._del(del_node, curr_root.right_child, dimension + 1)

        return curr_root

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

        axis = depth % self._dimension

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

        axis = depth % self._dimension

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

    def _minimum_node(self, root: Node, axis_target: int, axis_current: int) -> Union[Node, None]:
        """
        Find node with minimum item in Kd-tree by axis_target
        :param root: Current Node
        :param axis_target: Dimension by which we need to find the minimum element
        :param axis_current: Current Dimension
        :return: Minimum node or None
        """
        if root is None:
            return None
        if axis_target == axis_current:
            if root.left_child is None:
                return root
            return self._minimum_node(root.left_child, axis_target, (axis_current + 1) % self._dimension)

        right_min = self._minimum_node(root.right_child, axis_target, (axis_current + 1) % self._dimension)
        left_min = self._minimum_node(root.left_child, axis_target, (axis_current + 1) % self._dimension)
        result = root

        if right_min is not None and right_min.point[axis_target] < result.point[axis_target]:
            result = right_min
        if left_min is not None and left_min.point[axis_target] < result.point[axis_target]:
            result = left_min
        return result


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
