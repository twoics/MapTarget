from src.main.python.logic.point import Point
from src.main.python.logic.node import Node
from src.main.python.logic.tree import KdTree
import unittest


class TestPoint(unittest.TestCase):
    def test_init(self):
        point = Point(3, 4)

        self.assertEqual(point.x, 3)
        self.assertEqual(point.y, 4)

    def test_get_item(self):
        point = Point(1, 2)

        self.assertEqual(point[0], 1)
        self.assertEqual(point[1], 2)

    def test_setters(self):
        point = Point(1, 1)
        point.x = 2
        point.y = -1

        self.assertEqual(point.x, 2)
        self.assertEqual(point.y, -1)


class TestNode(unittest.TestCase):
    def test_init(self):
        point = Point(1, 1)
        node = Node(point)

        self.assertEqual(node.point, point)
        self.assertEqual(node.left_child, None)
        self.assertEqual(node.right_child, None)

    def test_left_child(self):
        root_node = Node()
        child_node = Node()

        self.assertEqual(root_node.left_child, None)
        root_node.left_child = child_node
        self.assertEqual(root_node.left_child, child_node)

    def test_right_child(self):
        root_node = Node()
        child_node = Node()

        self.assertEqual(root_node.right_child, None)
        root_node.right_child = child_node
        self.assertEqual(root_node.right_child, child_node)

    def test_point(self):
        node = Node()
        point = Point(12, 12)

        self.assertEqual(node.point, None)
        node.point = point
        self.assertEqual(node.point, point)


class TestTree(unittest.TestCase):
    def test_build(self):
        points_list = [Point(5, 4), Point(2, 6), Point(13, 3), Point(8, 7), Point(3, 1), Point(10, 2)]
        tree = KdTree(points_list)
        root = tree.get_root()

        self.assertEqual(root.point, points_list[3])
        self.assertEqual(root.left_child.point, points_list[0])

        self.assertEqual(root.left_child.left_child.point, points_list[4])
        self.assertEqual(root.left_child.left_child.left_child, None)
        self.assertEqual(root.left_child.left_child.right_child, None)

        self.assertEqual(root.left_child.right_child.point, points_list[1])
        self.assertEqual(root.left_child.right_child.left_child, None)
        self.assertEqual(root.left_child.right_child.right_child, None)

        self.assertEqual(root.right_child.point, points_list[2])
        self.assertEqual(root.right_child.right_child, None)

        self.assertEqual(root.right_child.left_child.point, points_list[-1])
        self.assertEqual(root.right_child.left_child.left_child, None)
        self.assertEqual(root.right_child.left_child.right_child, None)

    def test_closest_point(self):
        points_list = [Point(5, 4), Point(2, 6), Point(13, 3), Point(8, 7), Point(3, 1), Point(10, 2)]
        tree = KdTree(points_list)

        nearest_point = tree.closest_point(Point(9, 4))
        self.assertEqual(nearest_point, points_list[-1])


if __name__ == '__main__':
    unittest.main()
