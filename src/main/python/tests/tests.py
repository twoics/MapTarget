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

        self.assertEqual(root_node.right_child.point, child_1.point)
        self.assertEqual(root_node.left_child.point, child_2.point)

    def test_point(self):
        node = Node(Point(1, 1))
        point = Point(12, 12)

        self.assertEqual(node.point, Point(1, 1))
        node.point = point
        self.assertEqual(node.point, point)


class TestTree(unittest.TestCase):
    def test_build_1(self):
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

    def test_build_2(self):
        points_list = [Point(343, 858), Point(615, 40), Point(70, 721), Point(479, 449), Point(888, 585),
                       Point(207, 313), Point(751, 177)]

        tree = KdTree(points_list)
        root = tree.get_root()

        self.assertEqual(root.point, points_list[3])
        self.assertEqual(root.left_child.point, points_list[2])
        self.assertEqual(root.left_child.right_child.point, points_list[0])
        self.assertEqual(root.left_child.left_child.point, points_list[-2])

        self.assertEqual(root.left_child.right_child.left_child, None)
        self.assertEqual(root.left_child.right_child.right_child, None)

        self.assertEqual(root.left_child.left_child.left_child, None)
        self.assertEqual(root.left_child.left_child.right_child, None)

        self.assertEqual(root.right_child.point, points_list[-1])
        self.assertEqual(root.right_child.left_child.point, points_list[1])
        self.assertEqual(root.right_child.right_child.point, points_list[4])

        self.assertEqual(root.right_child.left_child.left_child, None)
        self.assertEqual(root.right_child.left_child.right_child, None)

        self.assertEqual(root.right_child.right_child.left_child, None)
        self.assertEqual(root.right_child.right_child.right_child, None)

    def test_closest_point_1(self):
        points_list = [Point(5, 4), Point(2, 6), Point(13, 3), Point(8, 7), Point(3, 1), Point(10, 2)]
        tree = KdTree(points_list)

        nearest_point = tree.closest_point(Point(9, 4))
        self.assertEqual(nearest_point, points_list[-1])

    def test_closest_point_2(self):
        points_list = [Point(343, 858), Point(615, 40), Point(70, 721), Point(479, 449), Point(888, 585),
                       Point(207, 313), Point(751, 177)]

        tree = KdTree(points_list)
        nearest_point = tree.closest_point(Point(438, 681))
        self.assertEqual(nearest_point, points_list[0])

    def test_add(self):
        points_list = [Point(5, 4), Point(2, 6), Point(13, 3), Point(8, 7), Point(3, 1), Point(10, 2)]
        tree = KdTree(points_list)
        root = tree.get_root()
        self.assertEqual(root.left_child.left_child.left_child, None)

        point_1 = Point(2, 3)
        point_2 = Point(4, 3)
        point_3 = Point(1, 5)
        point_4 = Point(6, 5)

        tree.add(point_1)
        tree.add(point_2)
        tree.add(point_3)
        tree.add(point_4)

        self.assertEqual(root.left_child.left_child.left_child.point, point_1)
        self.assertEqual(root.left_child.left_child.right_child.point, point_2)
        self.assertEqual(root.left_child.right_child.left_child.point, point_3)
        self.assertEqual(root.left_child.right_child.right_child.point, point_4)

    def test_del_1(self):
        tree = KdTree([Point(1, 1)])
        tree.remove(Point(1, 1))
        self.assertEqual(tree.get_root(), None)

    def test_del_2(self):
        points_list = [Point(5, 4), Point(2, 6), Point(13, 3), Point(8, 7), Point(3, 1), Point(10, 2)]
        tree = KdTree(points_list)
        root = tree.get_root()
        point_1 = Point(1, 5)
        point_2 = Point(6, 5)
        tree.add(point_1)
        tree.add(point_2)
        tree.remove(Point(2, 6))
        self.assertEqual(root.left_child.right_child.point, point_2)

    def test_del_3(self):
        tree = KdTree([Point(1, 1)])
        tree.remove(Point(1, 1))
        tree.remove(Point(2, 2))
        self.assertEqual(tree.get_root(), None)

    def test_del_4(self):
        points_list = [Point(5, 4), Point(2, 6), Point(13, 3), Point(8, 7), Point(3, 1), Point(10, 2)]
        tree = KdTree(points_list)
        root = tree.get_root()
        tree.remove(root.point)
        self.assertEqual(tree.get_root().point, Point(10, 2))

    def test_entry_1(self):
        points_list = [Point(5, 4), Point(2, 6), Point(13, 3), Point(8, 7), Point(3, 1), Point(10, 2)]
        tree = KdTree(points_list)
        res = tree.check_entry(Point(1, 2), Point(7, 10))
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0], Point(5, 4))
        self.assertEqual(res[1], Point(2, 6))

    def test_entry_2(self):
        points_list = [Point(5, 4), Point(2, 6), Point(13, 3), Point(8, 7), Point(3, 1), Point(10, 2)]
        tree = KdTree(points_list)
        res = tree.check_entry(Point(9, 1), Point(14, 3))
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0], Point(13, 3))
        self.assertEqual(res[1], Point(10, 2))


if __name__ == '__main__':
    unittest.main()
