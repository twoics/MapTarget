from src.main.python.tree.point import Point


class DataPoint:
    def __init__(self, point: Point, data: dict):
        self._point = point
        self._data = data

    @property
    def point(self) -> Point:
        return self._point

    @property
    def data(self) -> dict:
        return self._data

    @property
    def tuple_data(self) -> tuple:
        return self._point, self.data
