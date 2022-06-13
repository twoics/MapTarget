import unittest
from src.main.python.logic.point import Point
from src.main.python.logic.tree.node import Node
from src.main.python.logic.tree.tree import KdTree

DATA_SHORT = (
    (Point(5, 4), None),
    (Point(2, 6), None),
    (Point(13, 3), None),
    (Point(8, 7), None),
    (Point(3, 1), None),
    (Point(10, 2), None)
)
DATA_LONG = (
    (Point(343, 858), None),
    (Point(615, 40), None),
    (Point(70, 721), None),
    (Point(479, 449), None),
    (Point(888, 585), None),
    (Point(207, 313), None),
    (Point(751, 177), None)
)

DATA_SHORT_PARAM = (
    (Point(5, 4), None),
    (Point(2, 6), None),
    (Point(13, 3), None),
    (Point(8, 7), {"1": 1}),
    (Point(3, 1), None),
    (Point(10, 2), {"2": 2})
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
        node = Node(Point(1, 1))

        self.assertEqual(node.point, Point(1, 1))
        self.assertEqual(node.left_child, None)
        self.assertEqual(node.right_child, None)

    def test_left_child(self):
        root_node = Node(Point(1, 1))
        child_node = Node(Point(2, 2))

        self.assertEqual(root_node.left_child, None)
        root_node.left_child = child_node
        self.assertEqual(root_node.left_child, child_node)

    def test_right_child(self):
        root_node = Node(Point(1, 1))
        child_node = Node(Point(2, 2))

        self.assertEqual(root_node.right_child, None)
        root_node.right_child = child_node
        self.assertEqual(root_node.right_child, child_node)

    def test_two_child(self):
        root_node = Node(Point(1, 1))
        child_1 = Node(Point(2, 2))
        child_2 = Node(Point(3, 3))
        self.assertEqual(root_node.right_child, None)
        self.assertEqual(root_node.left_child, None)

        root_node.right_child = child_1
        root_node.left_child = child_2

        self.assertEqual(root_node.right_child, child_1)
        self.assertEqual(root_node.left_child, child_2)

        self.assertEqual(root_node.right_child, child_1)
        self.assertEqual(root_node.left_child, child_2)

    def test_point(self):
        node = Node(Point(1, 1))
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
        nearest_node = tree.closest_node(Point(9, 4))
        self.assertEqual(nearest_node.point, Point(10, 2))

    def test_closest_point_2(self):
        tree = KdTree(DATA_LONG)
        nearest_node = tree.closest_node(Point(438, 681))
        self.assertEqual(nearest_node.point, Point(343, 858))

    def test_add(self):
        tree = KdTree(DATA_SHORT)
        root = tree.get_root()
        self.assertEqual(root.left_child.left_child.left_child, None)

        tree.insert(Point(2, 3))
        tree.insert(Point(4, 3))
        tree.insert(Point(1, 5))
        tree.insert(Point(6, 5))

        self.assertEqual(root.left_child.left_child.left_child.point, Point(2, 3))
        self.assertEqual(root.left_child.left_child.right_child.point, Point(4, 3))
        self.assertEqual(root.left_child.right_child.left_child.point, Point(1, 5))
        self.assertEqual(root.left_child.right_child.right_child.point, Point(6, 5))

    def test_del_1(self):
        tree = KdTree(
            (
                (Point(1, 1), {}),
            )
        )
        tree.remove(Point(1, 1))
        self.assertEqual(tree.get_root(), None)

    def test_del_2(self):
        tree = KdTree(DATA_SHORT)
        root = tree.get_root()
        tree.insert(Point(1, 5))
        tree.insert(Point(6, 5))
        tree.remove(Point(2, 6))

        self.assertEqual(root.left_child.right_child.point, Point(6, 5))

    def test_del_3(self):
        tree = KdTree(
            (
                (Point(1, 1), {}),
            )
        )
        tree.remove(Point(1, 1))
        tree.remove(Point(1, 1))

        self.assertEqual(tree.get_root(), None)

    def test_del_4(self):
        tree = KdTree(DATA_SHORT_PARAM)
        tree.remove(Point(8, 7))
        self.assertEqual(tree.get_root().point, Point(10, 2))
        self.assertEqual(tree.get_root().data["2"], 2)

    def test_entry_1(self):
        tree = KdTree(DATA_SHORT)
        res = tree.check_entry(Point(1, 2), Point(7, 10))
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].point, Point(5, 4))
        self.assertEqual(res[1].point, Point(2, 6))

    def test_entry_2(self):
        tree = KdTree(DATA_SHORT)
        res = tree.check_entry(Point(9, 1), Point(14, 3))
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].point, Point(13, 3))
        self.assertEqual(res[1].point, Point(10, 2))

    def test_empty(self):
        t = KdTree()
        self.assertEqual(t.get_root(), None)
        t.insert(Point(123, 123), {'a': 123})
        self.assertEqual(t.get_root().point, Point(123, 123))
        self.assertEqual(t.get_root().data["a"], 123)
        t.remove(Point(123, 123))
        self.assertEqual(t.get_root(), None)
        t.remove(Point(11, 11))
        self.assertEqual(t.get_root(), None)
        self.assertEqual(t.check_entry(Point(123, 123), Point(123, 123)), [])
        self.assertEqual(t.closest_node(Point(3, 3)), None)
        self.assertEqual(t.rebuild_tree(DATA_SHORT).point, Point(8, 7))


if __name__ == '__main__':
    unittest.main()
