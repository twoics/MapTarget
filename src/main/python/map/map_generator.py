from src.main.python.tree.point import Point
from src.main.python.tree.tree_map import KdTreeMap
from src.main.python.map.queries import query_by_reserved, query_by_name, get_reserved
from src.main.python.map.map_initializer import pure_custom_map
from itertools import zip_longest
from typing import Union, Tuple, List
from .data_point import DataPoint
import folium
import overpy

MAP_POINT = Tuple[Union[float, int], Union[float, int], dict]

STANDARD_ICON = 'info-circle'
ICONS = {
    'cafe': 'coffee',
    'fast_food': 'cutlery',
    'restaurant': 'cutlery',
    'bar': 'beer',
    'cinema': 'film',
    'fitness': 'hand-rock-o',
    'museum': 'university',
    'library': 'book',
    'supermarket': 'shopping-basket',
    'clothes': 'shopping-bag',
    'mall': 'building',
    'electronic': 'calculator',
    'hospital': 'hospital-o',
    'fuel': 'tint',
    'hotel': 'bed',
    'pharmacy': 'plus-square',
}


# TODO Constant to JSON, create JSON connector

class Map:
    def __init__(self):
        # Data points is: [ DataPoint(), DataPoint()]
        self._data_points_list = None
        self._tree = KdTreeMap()
        self._query = None
        self._current_zoom = None

    def set_zoom(self, zoom: int) -> None:
        """
        Set zoom value
        This value is used when reloading
        the map to display the correct zoom
        :param zoom: Zoom value
        :return: None
        """
        self._current_zoom = zoom

    def pure_map(self) -> folium.Map:
        """
        Generate new Pure Map
        :return: Folium Map
        """
        new_map = pure_custom_map()
        self._data_points_list = None
        return new_map

    def generate_map(self, query: str, start_point: tuple, end_point: tuple) -> folium.Map:
        if len(start_point) != 2 or len(end_point) != 2:
            raise ValueError("Points must be 2-dimension tuple")
        if not all(isinstance(item, (float, int)) for item in start_point + end_point):
            raise ValueError("All points must be int or float")
        first_point = Point(start_point[0], start_point[1])
        second_point = Point(end_point[0], end_point[1])
        return self._generate_map(query, first_point, second_point)

    def find_closest(self, pivot: tuple) -> Union[folium.Map, None]:
        if len(pivot) != 2:
            raise ValueError("Points must be 2-dimension tuple")
        if not all(isinstance(item, (float, int)) for item in pivot):
            raise ValueError("All points must be int or float")
        point = Point(pivot[0], pivot[1])
        return self._find_closest(point)

    def _find_closest(self, pivot: Point) -> Union[folium.Map, None]:
        """
        Searches the current map for the nearest
        object to the point, then marks the nearest
        object to it, and returns a modified map
        :param pivot: The point for which the nearest object is searched for
        :return: Modified map
        """
        if not self._data_points_list:
            return None
        packed_data = pack_answer(self._data_points_list)
        self._tree.rebuild_tree(packed_data)

        closest = self._tree.closest_node(pivot)

        closest_point = closest.point

        new_map = self._build(closest_point, closest_point)

        # Here I add a user point to the map
        folium.Marker(
            pivot.points,
            icon=folium.Icon(
                icon=STANDARD_ICON,
                prefix="fa",
                color='red'),
            popup=f"<i>{'PIVOT'}</i>"
        ).add_to(new_map)

        return new_map

    def _generate_map(self, query: str, start_point: Point, end_point: Point) -> folium.Map:
        """
        Generates a folium map,
        if the query refers to a reserved type, (cafe, movie, gym)
        then searches for objects with that type,
        otherwise searches for objects by name
        :param query:
        :param start_point:
        :param end_point:
        :return:
        """
        if query in get_reserved():
            query_res = query_by_reserved(query, start_point.points, end_point.points)
        else:
            query_res = query_by_name(query, start_point.points, end_point.points)
        self._query = query
        return self._build_map_by_query(query_res, start_point, end_point)

    def _build_map_by_query(self, query: overpy.Result, start_point: Point, end_point: Point) -> folium.Map:
        """
        Builds a map, based on the result of the overpy.Result query
        :param query: Query result of overpy
        :return: New generated map
        """
        self._data_points_list = _unpack_query_answer(query)

        middle_point = start_point.middle_point(end_point)
        new_map = self._build(target_point=None, location=middle_point)
        return new_map

    def _build(self, target_point: Union[Point, None], location: Point) -> folium.Map:
        new_map = pure_custom_map(location=location, zoom=self._current_zoom)

        for point_obj in self._data_points_list:
            point_data = _get_html_point_info(point_obj.data)
            point = point_obj.point

            folium.Marker(
                # Set cords
                point.points,
                icon=folium.Icon(
                    icon=ICONS.get(self._query, STANDARD_ICON),
                    # TODO COMMENT THIS
                    color='green' if target_point and target_point == point else 'blue',
                    prefix="fa"),
                popup=folium.Popup(folium.IFrame(point_data),
                                   min_width=150,
                                   max_width=200)
            ).add_to(new_map)
        return new_map


def _unpack_query_answer(answer_query: overpy.Result) -> list:
    """
    Returns a list of points that show the location
    of an object on the map, by type of query
    :param answer_query: Query Result from overpy
    :return: List With points and data: [(latitude_1, longitude_1, {data_1}), (latitude_2, longitude_2, {data_2})]
    """
    data_points_list = []
    for node, way, rel in zip_longest(answer_query.nodes, answer_query.ways, answer_query.relations):
        if rel:
            data_points_list.append(
                DataPoint(
                    Point(float(rel.center_lat), float(rel.center_lon)), rel.tags
                )
            )
        if way:
            data_points_list.append(
                DataPoint(
                    Point(float(way.center_lat), float(way.center_lon)), way.tags
                )
            )
        if node:
            data_points_list.append(
                DataPoint(
                    Point(float(node.lat), float(node.lon)), node.tags
                )
            )
    return data_points_list


def _get_html_point_info(point_data: dict) -> str:
    """
    Return HTML for Marker PopUP
    :param point_data: Tags that contain a point
    :return: HTML as string
    """
    return f"""Name: {point_data.get('name', 'n/a')}<br>Amenity: {point_data.get('amenity', 'n/a')}"""


def pack_answer(unpacked_answer: List[DataPoint]) -> Tuple[Tuple[Point, Union[dict, None]], ...]:
    result = []
    for item in unpacked_answer:
        result.append(item.tuple_data)
    return tuple(result)
