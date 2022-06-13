from src.main.python.logic.point import Point
from src.main.python.logic.tree.tree_map import KdTreeMap
from src.main.python.logic.map.queries import query_by_reserved, query_by_name, get_reserved
from src.main.python.logic.map.web_source import JAVA_SCRIPT, HTML
from itertools import zip_longest
from src.main.python.logic.map.web_parser import WebParser
from typing import Union, Tuple, List
from src.main.python.logic.map.data_point import DataPoint
from src.main.python.json_connector import JsonConnector
from .map_interface import IMap
import folium
import overpy

MAP_POINT = Tuple[Union[float, int], Union[float, int], dict]

DEFAULT_ICON = 'info-circle'


class Map(IMap):
    INIT_LOCATION = [56.0140, 92.8563]
    STANDARD_ZOOM = 10

    def __init__(self):
        # [ DataPoint(), DataPoint()]
        self._points_on_map = None
        self._query = None
        self._tree = KdTreeMap()
        self._current_zoom = self.STANDARD_ZOOM

        # Icons for standard requests
        json_connector = JsonConnector()
        self._standard_icons = json_connector.get_icons()

    def update_current_zoom(self, zoom: int) -> None:
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
        new_map = self._pure_custom_map()
        self._points_on_map = None
        return new_map

    def find_objects(self, query: str, start_point: Point, end_point: Point) -> folium.Map:
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
        self._points_on_map = self._unpack_query_answer(query_res)

        middle_point = start_point.middle_point(end_point)
        new_map = self._build(target_point=None, location=middle_point)
        return new_map

    def nearest_object(self, pivot: Point) -> Union[folium.Map, None]:
        """
        Searches the current map for the nearest
        object to the point, then marks the nearest
        object to it, and returns a modified map
        :param pivot: The point for which the nearest object is searched for
        :return: Modified map
        """
        if not self._points_on_map:
            return None
        packed_data = self.pack_map_points(self._points_on_map)
        self._tree.rebuild_tree(packed_data)

        closest = self._tree.closest_node(pivot)

        closest_point = closest.point

        new_map = self._build(closest_point, closest_point)

        # Here I add a user point to the map
        folium.Marker(
            pivot.points,
            icon=folium.Icon(
                icon=DEFAULT_ICON,
                prefix="fa",
                color='red'),
            popup=f"<i>{'PIVOT'}</i>"
        ).add_to(new_map)

        return new_map

    def _build(self, target_point: Union[Point, None], location: Point) -> folium.Map:
        new_map = self._pure_custom_map(location=location, zoom=self._current_zoom)

        for point_obj in self._points_on_map:
            point_data = self._get_point_info(point_obj.data)
            point = point_obj.point

            folium.Marker(
                # Set cords
                point.points,
                icon=folium.Icon(
                    icon=self._standard_icons.get(self._query, DEFAULT_ICON),
                    # TODO COMMENT THIS
                    color='green' if target_point and target_point == point else 'blue',
                    prefix="fa"),
                popup=folium.Popup(folium.IFrame(point_data),
                                   min_width=150,
                                   max_width=200)
            ).add_to(new_map)
        return new_map

    def _pure_custom_map(self, location: Point = None, zoom: int = None) -> folium.Map:
        """
        Creates a new custom folium map,
        with the ability to draw on it
        :return: Pure Folium map
        """
        current_location = location.points if location else self.INIT_LOCATION
        current_zoom = zoom if zoom else self._current_zoom

        f_map = folium.Map(location=current_location,
                           zoom_start=current_zoom)

        custom_html = WebParser(html=HTML)
        custom_js = WebParser(script=JAVA_SCRIPT, args={'map': f_map.get_name()})

        f_map.get_root().add_child(custom_html)
        f_map.add_child(custom_js)

        return f_map

    @staticmethod
    def _unpack_query_answer(answer_query: overpy.Result) -> list:
        """
        Returns a list of points that show the location
        of an object on the map, by type of query
        :param answer_query: Query Result from overpy
        :return: Data Points list
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

    @staticmethod
    def _get_point_info(point_data: dict) -> str:
        """
        Return HTML for Marker PopUP
        :param point_data: Tags that contain a point
        :return: HTML as string
        """
        return f"""Name: {point_data.get('name', 'n/a')}<br>Amenity: {point_data.get('amenity', 'n/a')}"""

    @staticmethod
    def pack_map_points(unpacked_answer: List[DataPoint]) -> Tuple[Tuple[Point, Union[dict, None]], ...]:
        result = []
        for item in unpacked_answer:
            result.append(item.tuple_data)
        return tuple(result)
