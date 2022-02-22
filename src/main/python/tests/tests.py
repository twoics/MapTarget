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
        nodes_list = [Node((5, 4)), Node((2, 6)), Node((13, 3)), Node((8, 7)), Node((3, 1)), Node((10, 2))]
        tree = KdTree(nodes_list)
        root = tree.get_root()

        self.assertEqual(root, nodes_list[3])
        self.assertEqual(root.left_child, nodes_list[0])

        self.assertEqual(root.left_child.left_child, nodes_list[4])
        self.assertEqual(root.left_child.left_child.left_child, None)
        self.assertEqual(root.left_child.left_child.right_child, None)

        self.assertEqual(root.left_child.right_child, nodes_list[1])
        self.assertEqual(root.left_child.right_child.left_child, None)
        self.assertEqual(root.left_child.right_child.right_child, None)

        self.assertEqual(root.right_child, nodes_list[2])
        self.assertEqual(root.right_child.right_child, None)

        self.assertEqual(root.right_child.left_child, nodes_list[-1])
        self.assertEqual(root.right_child.left_child.left_child, None)
        self.assertEqual(root.right_child.left_child.right_child, None)

    def test_build_2(self):
        nodes_list = [Node((343, 858)), Node((615, 40)), Node((70, 721)), Node((479, 449)), Node((888, 585)),
                      Node((207, 313)), Node((751, 177))]

        tree = KdTree(nodes_list)
        root = tree.get_root()

        self.assertEqual(root, nodes_list[3])
        self.assertEqual(root.left_child, nodes_list[2])
        self.assertEqual(root.left_child.right_child, nodes_list[0])
        self.assertEqual(root.left_child.left_child, nodes_list[-2])

        self.assertEqual(root.left_child.right_child.left_child, None)
        self.assertEqual(root.left_child.right_child.right_child, None)

        self.assertEqual(root.left_child.left_child.left_child, None)
        self.assertEqual(root.left_child.left_child.right_child, None)

        self.assertEqual(root.right_child, nodes_list[-1])
        self.assertEqual(root.right_child.left_child, nodes_list[1])
        self.assertEqual(root.right_child.right_child, nodes_list[4])

        self.assertEqual(root.right_child.left_child.left_child, None)
        self.assertEqual(root.right_child.left_child.right_child, None)

        self.assertEqual(root.right_child.right_child.left_child, None)
        self.assertEqual(root.right_child.right_child.right_child, None)

    def test_closest_point_1(self):
        nodes_list = [Node((5, 4)), Node((2, 6)), Node((13, 3)), Node((8, 7)), Node((3, 1)), Node((10, 2))]
        tree = KdTree(nodes_list)

        nearest_point = tree.closest_node(Point(9, 4))
        self.assertEqual(nearest_point, nodes_list[-1])

    def test_closest_point_2(self):
        nodes_list = [Node((343, 858)), Node((615, 40)), Node((70, 721)), Node((479, 449)), Node((888, 585)),
                      Node((207, 313)), Node((751, 177))]

        tree = KdTree(nodes_list)
        nearest_point = tree.closest_node(Point(438, 681))
        self.assertEqual(nearest_point, nodes_list[0])

    def test_add(self):
        points_list = [Node((5, 4)), Node((2, 6)), Node((13, 3)), Node((8, 7)), Node((3, 1)), Node((10, 2))]
        tree = KdTree(points_list)
        root = tree.get_root()
        self.assertEqual(root.left_child.left_child.left_child, None)

        point_1 = Node((2, 3))
        point_2 = Node((4, 3))
        point_3 = Node((1, 5))
        point_4 = Node((6, 5))

        tree.insert(point_1)
        tree.insert(point_2)
        tree.insert(point_3)
        tree.insert(point_4)

        self.assertEqual(root.left_child.left_child.left_child.point, point_1.point)
        self.assertEqual(root.left_child.left_child.right_child.point, point_2.point)
        self.assertEqual(root.left_child.right_child.left_child.point, point_3.point)
        self.assertEqual(root.left_child.right_child.right_child.point, point_4.point)

    def test_del_1(self):
        node = Node((1, 1))
        tree = KdTree([node])
        tree.remove(node)
        self.assertEqual(tree.get_root(), None)

    def test_del_2(self):
        nodes_list = [Node((5, 4)), Node((2, 6)), Node((13, 3)), Node((8, 7)), Node((3, 1)), Node((10, 2))]
        tree = KdTree(nodes_list)
        root = tree.get_root()
        node_1 = Node((1, 5))
        node_2 = Node((6, 5))
        tree.insert(node_1)
        tree.insert(node_2)
        tree.remove(nodes_list[1])

        self.assertEqual(root.left_child.right_child.point, node_2.point)

    def test_del_3(self):
        node = Node((1, 1))
        tree = KdTree([node])
        tree.remove(node)
        tree.remove(node)
        self.assertEqual(tree.get_root(), None)

    def test_del_4(self):
        nodes_list = [Node((5, 4)), Node((2, 6)), Node((13, 3)), Node((8, 7), data="1"), Node((3, 1)),
                      Node((10, 2), data="2")]
        tree = KdTree(nodes_list)
        root = tree.get_root()
        tree.remove(root)
        self.assertEqual(tree.get_root().point, Point(10, 2))
        self.assertEqual(tree.get_root().data, "2")

    def test_entry_1(self):
        nodes_list = [Node((5, 4)), Node((2, 6)), Node((13, 3)), Node((8, 7)), Node((3, 1)), Node((10, 2))]
        tree = KdTree(nodes_list)
        res = tree.check_entry(Point(1, 2), Point(7, 10))
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].point, Point(5, 4))
        self.assertEqual(res[1].point, Point(2, 6))

    def test_entry_2(self):
        nodes_list = [Node((5, 4)), Node((2, 6)), Node((13, 3)), Node((8, 7)), Node((3, 1)), Node((10, 2))]
        tree = KdTree(nodes_list)
        res = tree.check_entry(Point(9, 1), Point(14, 3))
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].point, Point(13, 3))
        self.assertEqual(res[1].point, Point(10, 2))


if __name__ == '__main__':
    unittest.main()
