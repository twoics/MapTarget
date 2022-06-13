from typing import Tuple, Union, List
from overpy.exception import OverpassTooManyRequests, OverpassGatewayTimeout
from ...json_connector import JsonConnector

import overpy
import time
import logging

POINT = Tuple[Union[int, float], Union[int, float]]

API = overpy.Overpass()

SHORT_BREAK = 1
LONG_BREAK = 5

json_connector = JsonConnector()

RESERVED_QUERY = json_connector.get_standard_queries()


def query_by_name(name: str, start_point: POINT, end_point: POINT) -> overpy.Result:
    """
    Returns the result of a query for this name
    :param name: The name by which to search for objects on the map
    :param start_point: Search starting point
    :param end_point: Ending starting point
    :return: Returns overpy.Result by name query, starting from start_point to end_point
    """
    return _query_answer(f"""
        (node["name"="{name}"]({start_point[0]}, {start_point[1]}, {end_point[0]}, {end_point[1]});
         way["name"="{name}"]({start_point[0]}, {start_point[1]}, {end_point[0]}, {end_point[1]});
         relation["name"="{name}"]({start_point[0]}, {start_point[1]}, {end_point[0]}, {end_point[1]}););
        out center;
        """)


def query_by_category(category: str, target_obj: str, start_point: POINT, end_point: POINT) -> overpy.Result:
    """
    Returns the result of a query for a specific category object
    :param category: Category type like - amenity, tourism...
    :param target_obj: The object you want to find, of the selected category like - hospital, hotel...
    :param start_point: Search starting point
    :param end_point: Ending starting point
    :return: Returns overpy.Result by target_obj type of category
    """
    return _query_answer(f"""
        (node[{category}={target_obj}]({start_point[0]}, {start_point[1]}, {end_point[0]}, {end_point[1]});
         way[{category}={target_obj}]({start_point[0]}, {start_point[1]}, {end_point[0]}, {end_point[1]});
         relation[{category}={target_obj}]({start_point[0]}, {start_point[1]}, {end_point[0]}, {end_point[1]}););
        out center;
    """)


def query_by_reserved(query: str, start_point: POINT, end_point: POINT) -> Union[overpy.Result, None]:
    """
    Returns the result from a reserved query
    :param query: Reserved word for the query, they can be obtained from get_reserved
    :param start_point: Search starting point
    :param end_point: Ending starting point
    :return: overpy.Result on a reserved query, if a word is passed that is not in reserved, it returns None
    """
    if query not in RESERVED_QUERY:
        return None
    category, target_obj = RESERVED_QUERY.get(query)
    return query_by_category(category, target_obj, start_point, end_point)


def get_reserved() -> List[str]:
    """
    :return: A list of all reserved queries
    """
    return [key for key in RESERVED_QUERY]


def _query_answer(query: str) -> overpy.Result:
    """
    Waits for a response from overpy until it gets a result,
    if it catches an exception exceeding the wait time
    starts the query again
    :param query: Query to overpy
    :return: overpy.Result
    """
    while True:
        try:
            query_result = API.query(query)
        except OverpassTooManyRequests:
            logging.warning("So many requests, but query still running")
            time.sleep(SHORT_BREAK)
            continue
        except OverpassGatewayTimeout:
            logging.warning("Gateway Timeout, query is reload")
            time.sleep(LONG_BREAK)
            continue
        return query_result
