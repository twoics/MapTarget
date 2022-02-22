from src.main.python.logic.point import Point
from src.main.python.logic.node import Node
from src.main.python.logic.tree import KdTree
import unittest

DATA_SHORT = (
    (5, 4, None),
    (2, 6, None),
    (13, 3, None),
    (8, 7, None),
    (3, 1, None),
    (10, 2, None)
)
DATA_LONG = (
    (343, 858, None),
    (615, 40, None),
    (70, 721, None),
    (479, 449, None),
    (888, 585, None),
    (207, 313, None),
    (751, 177, None)
)

DATA_SHORT_PARAM = (
    (5, 4, None),
    (2, 6, None),
    (13, 3, None),
    (8, 7, {"1": 1}),
    (3, 1, None),
    (10, 2, {"2": 2})
)


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
        node = Node((1, 1))

        self.assertEqual(node.point, Point(1, 1))
        self.assertEqual(node.left_child, None)
        self.assertEqual(node.right_child, None)

    def test_left_child(self):
        root_node = Node((1, 1))
        child_node = Node((2, 2))

        self.assertEqual(root_node.left_child, None)
        root_node.left_child = child_node
        self.assertEqual(root_node.left_child, child_node)

    def test_right_child(self):
        root_node = Node((1, 1))
        child_node = Node((2, 2))

        self.assertEqual(root_node.right_child, None)
        root_node.right_child = child_node
        self.assertEqual(root_node.right_child, child_node)

    def test_two_child(self):
        root_node = Node((1, 1))
        child_1 = Node((2, 2))
        child_2 = Node((3, 3))
        self.assertEqual(root_node.right_child, None)
        self.assertEqual(root_node.left_child, None)

        root_node.right_child = child_1
        root_node.left_child = child_2

        self.assertEqual(root_node.right_child, child_1)
        self.assertEqual(root_node.left_child, child_2)

        self.assertEqual(root_node.right_child, child_1)
        self.assertEqual(root_node.left_child, child_2)

    def test_point(self):
        node = Node((1, 1))
        point = Point(12, 12)

        self.assertEqual(node.point, Point(1, 1))
        node.point = point
        self.assertEqual(node.point, point)


class TestTree(unittest.TestCase):
    def test_build_1(self):
        tree = KdTree(DATA_SHORT)
        root = tree.get_root()

        self.assertEqual(root.point, Point(8, 7))
        self.assertEqual(root.left_child.point, Point(5, 4))

        self.assertEqual(root.left_child.left_child.point, Point(3, 1))
        self.assertEqual(root.left_child.left_child.left_child, None)
        self.assertEqual(root.left_child.left_child.right_child, None)

        self.assertEqual(root.left_child.right_child.point, Point(2, 6))
        self.assertEqual(root.left_child.right_child.left_child, None)
        self.assertEqual(root.left_child.right_child.right_child, None)

        self.assertEqual(root.right_child.point, Point(13, 3))
        self.assertEqual(root.right_child.right_child, None)

        self.assertEqual(root.right_child.left_child.point, Point(10, 2))
        self.assertEqual(root.right_child.left_child.left_child, None)
        self.assertEqual(root.right_child.left_child.right_child, None)

    def test_build_2(self):
        tree = KdTree(DATA_LONG)
        root = tree.get_root()

        self.assertEqual(root.point, Point(479, 449))
        self.assertEqual(root.left_child.point, Point(70, 721))
        self.assertEqual(root.left_child.right_child.point, Point(343, 858))
        self.assertEqual(root.left_child.left_child.point, Point(207, 313))

        self.assertEqual(root.left_child.right_child.left_child, None)
        self.assertEqual(root.left_child.right_child.right_child, None)

        self.assertEqual(root.left_child.left_child.left_child, None)
        self.assertEqual(root.left_child.left_child.right_child, None)

        self.assertEqual(root.right_child.point, Point(751, 177))
        self.assertEqual(root.right_child.left_child.point, Point(615, 40))
        self.assertEqual(root.right_child.right_child.point, Point(888, 585))

        self.assertEqual(root.right_child.left_child.left_child, None)
        self.assertEqual(root.right_child.left_child.right_child, None)

        self.assertEqual(root.right_child.right_child.left_child, None)
        self.assertEqual(root.right_child.right_child.right_child, None)

    def test_closest_point_1(self):
        tree = KdTree(DATA_SHORT)
        nearest_node = tree.closest_node(9, 4)
        self.assertEqual(nearest_node.point, Point(10, 2))

    def test_closest_point_2(self):
        tree = KdTree(DATA_LONG)
        nearest_node = tree.closest_node(438, 681)
        self.assertEqual(nearest_node.point, Point(343, 858))

    def test_add(self):
        tree = KdTree(DATA_SHORT)
        root = tree.get_root()
        self.assertEqual(root.left_child.left_child.left_child, None)

        tree.insert(2, 3)
        tree.insert(4, 3)
        tree.insert(1, 5)
        tree.insert(6, 5)

        self.assertEqual(root.left_child.left_child.left_child.point, Point(2, 3))
        self.assertEqual(root.left_child.left_child.right_child.point, Point(4, 3))
        self.assertEqual(root.left_child.right_child.left_child.point, Point(1, 5))
        self.assertEqual(root.left_child.right_child.right_child.point, Point(6, 5))

    def test_del_1(self):
        tree = KdTree(
            (
                (1, 1, {}),
            )
        )
        tree.remove(1, 1)
        self.assertEqual(tree.get_root(), None)

    def test_del_2(self):
        tree = KdTree(DATA_SHORT)
        root = tree.get_root()
        tree.insert(1, 5)
        tree.insert(6, 5)
        tree.remove(2, 6)

        self.assertEqual(root.left_child.right_child.point, Point(6, 5))

    def test_del_3(self):
        tree = KdTree(
            (
                (1, 1, {}),
            )
        )
        tree.remove(1, 1)
        tree.remove(1, 1)

        self.assertEqual(tree.get_root(), None)

    def test_del_4(self):
        tree = KdTree(DATA_SHORT_PARAM)
        tree.remove(8, 7)
        self.assertEqual(tree.get_root().point, Point(10, 2))
        self.assertEqual(tree.get_root().data["2"], 2)

    def test_entry_1(self):
        tree = KdTree(DATA_SHORT)
        res = tree.check_entry((1, 2), (7, 10))
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].point, Point(5, 4))
        self.assertEqual(res[1].point, Point(2, 6))

    def test_entry_2(self):
        tree = KdTree(DATA_SHORT)
        res = tree.check_entry((9, 1), (14, 3))
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].point, Point(13, 3))
        self.assertEqual(res[1].point, Point(10, 2))

    def test_empty(self):
        t = KdTree()
        self.assertEqual(t.get_root(), None)
        t.insert(123, 123, {'a': 123})
        self.assertEqual(t.get_root().point, Point(123, 123))
        self.assertEqual(t.get_root().data["a"], 123)
        t.remove(123, 123)
        self.assertEqual(t.get_root(), None)
        t.remove(11, 11)
        self.assertEqual(t.get_root(), None)
        self.assertEqual(t.check_entry((123, 123), (123, 123)), [])
        self.assertEqual(t.closest_node(3, 3), None)
        self.assertEqual(t.rebuild_tree(DATA_SHORT).point, Point(8, 7))


if __name__ == '__main__':
    unittest.main()
