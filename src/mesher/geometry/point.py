from .abc import IPoint

# The tolerance that the x- and y-positions should be within in order to be considered
# equal when comparing two points.
TOL: float = 1e-10


class Point(IPoint):

    """
    This represents a two-dimensional point with an ID attached so the user can see
    which figure the point is a part of after meshing.

    Attributes:
        ID:     The ID of the point.
        x:      The x-position of the point (in meters).
        y:      The y-position of the point (in meters).
    """

    def __init__(self, *, x: float, y: float, ID: int) -> None:
        """
        Constructor...

        Example:
            ```py
            >>> from mesher.geometry.point import Point
            >>> point = Point(x=3.2, y=-4.6, ID=47)
            >>> point.x
            3.2
            >>> point.y
            -4.6
            >>> point.ID
            47
            ```

        Args:
            x:
                The x-position of the point (in meters).
            y:
                The y-position of the point (in meters).
            ID:
                The ID of the point.
        """

        self._ID: int = ID
        """
        The ID of the point. If the point is user-generated, it should be positive. If
        the point is generated somewhere within the code, it should be negative.

        Type:
            int
        """

        self._x: float = x
        """
        The x-position of the point (in meters).

        Type:
            float
        """

        self._y: float = y
        """
        The y-position of the point (in meters)
        """

    def __eq__(self, other: IPoint) -> bool:
        """
        This checks to see if two points have the same x- and y-positions (within a
        certain tolerance) regardless of their ID.

        TODO: update this when we can handle other units (e.g., feet, cm, ...)?

        Example:
            ```py
            >>> point1 = Point(x=6.5, y=-7.6, ID=1)
            >>> point2 = Point(x=6.5, y=-7.6, ID=2)
            >>> point1 == point2
            True
            >>> point3 = Point(x=6.5, y=-7.7, ID=3)
            >>> point1 == point3
            False
            ```

        Args:
            other:
                ...

        Returns:
            flag:
                ...
        """

        return abs(self._x - other.x) < TOL and abs(self._y - other.y) < TOL

    def __str__(self) -> str:
        """
        This prints the current point instance to the screen.

        Example:
            ```py
            >>> print(point)
            Point(x=3.2, y=-4.6, ID=47)
            ```

        Returns:
            ret:
                ...
        """

        return f"Point(x={self._x}, y={self._y}, ID={self._ID})"

    @property
    def ID(self) -> int:
        """This gets the ID of the point."""

        return self._ID

    @property
    def x(self) -> float:
        """This gets the x-position of the point."""

        return self._x

    @property
    def y(self) -> float:
        """This gets the y-position of the point."""

        return self._y
