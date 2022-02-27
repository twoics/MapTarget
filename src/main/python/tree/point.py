"""
Module implementing the point of node location
"""


class Point:
    """
    Class implementing the Point of Node location
    """

    def __init__(self, x: float = None, y: float = None):
        self._x = x
        self._y = y

    def __str__(self):
        return f"({self._x}, {self._y})"

    def __getitem__(self, item):
        if item == 0:
            return self._x
        elif item == 1:
            return self._y
        raise Exception("Only 0 or 1 expected")

    def __eq__(self, other):
        if isinstance(other, Point):
            if other.x == self._x and other.y == self._y:
                return True
            return False
        # Else compare as object

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, new_x: float):
        self._x = new_x

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, new_y: float):
        self._y = new_y
