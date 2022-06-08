# Standard library import
import math

# Local application imports
from .tree import KdTree
from .node import Node


class KdTreeMap(KdTree):
    EARTH_RADIUS = 6372795
    PI = math.pi

    def _node_distance(self, node_1: Node, node_2: Node) -> float:
        """
        Calculates the distance between two points on the sphere,
        necessary to search on the map
        :param node_1: First point
        :param node_2: Second point
        :return: Distance between points on map
        """
        lat_1 = node_1.point[0] * self.PI / 180
        lon_1 = node_1.point[1] * self.PI / 180
        lat_2 = node_2.point[0] * self.PI / 180
        lon_2 = node_2.point[1] * self.PI / 180

        cl1 = math.cos(lat_1)
        cl2 = math.cos(lat_2)
        sl1 = math.sin(lat_1)
        sl2 = math.sin(lat_2)

        delta = lon_2 - lon_1
        cos_delta = math.cos(delta)
        sin_delta = math.sin(delta)

        y = math.sqrt(pow(cl2 * sin_delta, 2) + pow(cl1 * sl2 - sl1 * cl2 * cos_delta, 2))
        x = sl1 * sl2 + cl1 * cl2 * cos_delta

        ad = math.atan2(y, x)
        dist = ad * self.EARTH_RADIUS

        return dist
