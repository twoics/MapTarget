from typing import Union, List, Tuple
from .node import Node
from .point import Point

import math

INIT_TREE = Tuple[Tuple[Union[float, int], Union[float, int], Union[dict, None]], ...]
POINT = Tuple[Union[float, int], Union[float, int]]
GEOGRAPHIC_COORDINATE = Union[float, int]

EARTH_RADIUS = 6372795
PI = math.pi


def unpack(data: INIT_TREE) -> List[Node]:
    """
    Unpack INIT_TREE to Node list
    :param data: Init tuple with points
    :return: Nodes List
    """
    nodes = []
    for tup in data:
        new_node = Node((tup[0], tup[1]), data=tup[2])
        nodes.append(new_node)
    return nodes


def nearest_node(pivot: Point, node_1: Union[Node, None], node_2: [Node, None]) -> Union[Node, None]:
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

    pivot_node = Node((pivot.x, pivot.y))

    distance_1 = euclidean_distance_node(pivot_node, node_1)
    distance_2 = euclidean_distance_node(pivot_node, node_2)

    if distance_1 < distance_2:
        return node_1
    else:
        return node_2


def euclidean_distance_node(node_1: Node, node_2: Node) -> float:
    """
    Calculate euclidean distance by 2 points
    :param node_1: First point
    :param node_2: Second point
    :return: Euclidean distance
    """
    x1, y1 = node_1.point[0], node_1.point[1]
    x2, y2 = node_2.point[0], node_2.point[1]

    delta_x = x1 - x2
    delta_y = y1 - y2

    return math.sqrt(delta_x ** 2 + delta_y ** 2)


def sphere_distance(lat_1, lon_1, lat_2, lon_2) -> float:
    """
    Calculates the distance between two points on the sphere, necessary to search on the map
    :param lat_1: Latitude of the first point
    :param lon_1: Longitude of the first point
    :param lat_2: Latitude of the second point
    :param lon_2: Longitude of the second point
    :return: Distance between points on map
    """
    lat1 = lat_1 * PI / 180
    lat2 = lat_2 * PI / 180
    long1 = lon_1 * PI / 180
    long2 = lon_2 * PI / 180

    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)

    delta = long2 - long1
    cos_delta = math.cos(delta)
    sin_delta = math.sin(delta)

    y = math.sqrt(pow(cl2 * sin_delta, 2) + pow(cl1 * sl2 - sl1 * cl2 * cos_delta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cos_delta

    ad = math.atan2(y, x)
    dist = ad * EARTH_RADIUS

    return dist


def nearest_node_map(pivot: Point, node_1: Union[Node, None], node_2: [Node, None]) -> Union[Node, None]:
    """
    Counts the distance between two points on the map
    :param pivot: The point to which we are looking for the closest
    :param node_1: First node
    :param node_2: Second node
    :return: Nearest node to pivot on MAP
    """
    if node_1 is None:
        return node_2

    if node_2 is None:
        return node_1

    pivot_node = Node((pivot.x, pivot.y))

    distance_1 = sphere_distance(pivot_node.point[0], pivot_node.point[1], node_1.point[0], node_1.point[1])
    distance_2 = sphere_distance(pivot_node.point[0], pivot_node.point[1], node_2.point[0], node_2.point[1])

    if distance_1 < distance_2:
        return node_1
    else:
        return node_2
