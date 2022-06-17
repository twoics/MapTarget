"""
Module implementing the k-d tree
"""

# Standard library import
from typing import Union, Tuple, List

# Local application imports
from ..point import Point
from .node import Node


class KdTree:
    """
    The class that implements KD tree
    """
    INIT_TREE = Tuple[Tuple[Point, Union[dict, None]], ...]

    # Since this tree was built for the map, the space is two-dimensional
    DIMENSION = 2

    def __init__(self, init_data: INIT_TREE = None):
        """
        Builds a k-d tree based on the tuple of Points and Data
        :param init_data: Tuple with points and data by which to build a tree
        """
        self._output_str = ""

        # Build tree if init nodes is not None
        self._root_node = self._build_tree(self.unpack(init_data)) if init_data is not None else None

    def __str__(self):
        self._output_str = ""
        self._tree_to_str(self._root_node)
        return self._output_str

    def get_root(self) -> Node:
        """
        :return: Root Node of KD tree
        """
        return self._root_node

    def insert(self, point: Point, data: dict = None) -> None:
        """
        Insert node with Point coordinates into k-d tree
        :param point: Point to insert
        :param data: Data to set by the node
        :return: None
        """
        node = Node(point, data=data)
        if self._root_node:
            self._add(node, self._root_node)
        else:
            self._root_node = node

    def remove(self, point: Point) -> None:
        """
        Removes a node with point coordinates from the k-d tree
        :param point: Point to delete
        :return: None
        """
        node = Node(point)
        if node is None or self._root_node is None:
            return
        elif self._root_node.left_child is None and self._root_node.right_child is None and node.point == \
                self._root_node.point:
            self._root_node = None
        else:
            self._del(node, self._root_node)

    def closest_node(self, point: Point) -> Union[Node, None]:
        """
        Searches for the nearest node of the point
        :param point: Pivot point
        :return: Nearest Point
        """
        return self._closest_node(self._root_node, point)

    def check_entry(self, start_point: Point, end_point: Point) -> list:
        """
        Outputs a list of nodes that are included in
        the area from start_point to end_point
        :param start_point: First point
        :param end_point: Second point
        :return: List with nodes
        """
        if start_point.x > end_point.x or start_point.y > end_point.y:
            raise ValueError("First point must be less then second")
        nodes_in_area = []
        self._entry_field(start_point, end_point, self._root_node, nodes_in_area)

        # nodes_in_area has been changed !
        return nodes_in_area

    def rebuild_tree(self, init_data: INIT_TREE) -> Union[Node, None]:
        """
        Rebuild KD tree by points
        :param init_data: Tuple with points and data by which to build a tree
        :return: Root Node of KD-tree
        """
        nodes = self.unpack(init_data)
        self._root_node = self._build_tree(nodes)
        return self._root_node

    def _node_distance(self, node_1: Node, node_2: Node) -> float:
        """
        Calculate euclidean distance by 2 points
        :param node_1: First point
        :param node_2: Second point
        :return: Euclidean distance
        """
        point_1 = node_1.point
        point_2 = node_2.point
        return point_1.euclidean_distance(point_2)

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

        axis = depth % self.DIMENSION
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

        dimension = dimension % self.DIMENSION

        if del_node.point == curr_root.point:

            if curr_root.right_child is not None:
                right_min = self._minimum_node(curr_root.right_child, dimension, dimension + 1)

                curr_root.point = right_min.point
                curr_root.data = right_min.data
                curr_root.right_child = self._del(right_min, curr_root.right_child, dimension + 1)

            elif curr_root.left_child is not None:
                left_min = self._minimum_node(curr_root.left_child, dimension, dimension + 1)

                curr_root.point = left_min.point
                curr_root.data = left_min.data

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

    def _closest_node(self, root: Node, point: Point, depth=0) -> Union[Node, None]:
        """
        Calculate the closest node to pivot
        :param root: Root node of K-d tree
        :param point: The point to which we are looking for the closest
        :param depth: Recursive parameter
        :return: Closest Point
        """

        if root is None:
            return None

        axis = depth % self.DIMENSION

        if point[axis] < root.point[axis]:
            next_branch = root.left_child
            opposite_branch = root.right_child
        else:
            next_branch = root.right_child
            opposite_branch = root.left_child

        best = self._nearest_node(point,
                                  self._closest_node(
                                      next_branch,
                                      point,
                                      depth + 1
                                  ),
                                  root)

        node_point = Node(Point(point.x, point.y))

        # If distance from pivot to 'best' node bigger than module by distance(perpendicular)
        # from pivot to space section -> check opposite branch (maybe there is a node closer)
        if self._node_distance(node_point, best) > abs(point[axis] - root.point[axis]):
            best = self._nearest_node(point,
                                      self._closest_node(
                                          opposite_branch,
                                          point,
                                          depth + 1
                                      ),
                                      best
                                      )

        return best

    def _nearest_node(self, pivot: Point, node_1: Union[Node, None], node_2: [Node, None]) -> Union[Node, None]:
        """
        Returns the node that is closer to the pivot
        :param pivot: The point to which we are looking for the closest
        :param node_1: First node
        :param node_2: Second node
        :return: Nearest node to pivot
        """
        if node_1 is None:
            return node_2

        if node_2 is None:
            return node_1

        pivot_node = Node(Point(pivot.x, pivot.y))

        distance_1 = self._node_distance(pivot_node, node_1)
        distance_2 = self._node_distance(pivot_node, node_2)

        if distance_1 < distance_2:
            return node_1
        else:
            return node_2

    def _build_tree(self, nodes_list: List[Node], depth=0, parent: Node = None) -> Union[Node, None]:
        """
        Builds a k-d tree
        :param nodes_list: The list of points from which to build the tree
        :param depth: Recursive parameter
        :param parent: Recursive parameter
        :return:
        """
        length = len(nodes_list)

        if length <= 0:
            return None

        axis = depth % self.DIMENSION

        # Sort point by axis (by 'x' or 'y' )
        sorted_points = [node for node in sorted(nodes_list, key=lambda node: node.point[axis])]

        root = sorted_points[length // 2]

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

    def _entry_field(self, start_pos: Point, end_pos: Point, node: Node, nodes_in_area: list, depth=0) -> None:
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

        axis = depth % self.DIMENSION
        point = node.point

        if point[axis] > start_pos[axis] and point[axis] > end_pos[axis]:  # Area left or down
            self._entry_field(start_pos, end_pos, node.left_child, nodes_in_area, depth + 1)
        elif point[axis] < start_pos[axis] and point[axis] < end_pos[axis]:  # Area right or up
            self._entry_field(start_pos, end_pos, node.right_child, nodes_in_area, depth + 1)
        else:  # Area across axis
            if start_pos.x <= point.x <= end_pos.x and start_pos.y <= point.y <= end_pos.y:  # Point in area
                nodes_in_area.append(node)
            self._entry_field(start_pos, end_pos, node.left_child, nodes_in_area, depth + 1)
            self._entry_field(start_pos, end_pos, node.right_child, nodes_in_area, depth + 1)

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
            return self._minimum_node(root.left_child, axis_target, (axis_current + 1) % self.DIMENSION)

        right_min = self._minimum_node(root.right_child, axis_target, (axis_current + 1) % self.DIMENSION)
        left_min = self._minimum_node(root.left_child, axis_target, (axis_current + 1) % self.DIMENSION)
        result = root

        if right_min is not None and right_min.point[axis_target] < result.point[axis_target]:
            result = right_min
        if left_min is not None and left_min.point[axis_target] < result.point[axis_target]:
            result = left_min
        return result

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

    @staticmethod
    def unpack(data: INIT_TREE) -> List[Node]:
        """
        Unpack INIT_TREE to Node list
        :param data: Init tuple with points
        :return: Nodes List
        """
        nodes = []
        for tup in data:
            new_node = Node(tup[0], data=tup[1])
            nodes.append(new_node)
        return nodes
