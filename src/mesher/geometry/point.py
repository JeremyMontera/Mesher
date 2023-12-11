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

        Args:
            x:
                The x-position of the point (in meters).
            y:
                The y-position of the point (in meters).
            ID:
                The ID of the point.

        Example:
            ```py
            >>> point = Point(x=3.2, y=-4.6, ID=47)
            >>> point.x
            3.2
            >>> point.y
            -4.6
            >>> point.ID
            47
            ```
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

    def __add__(self, other: IPoint) -> IPoint:
        """
        This adds together two points component-wise. This will assign the new point
        an ID corresponding to the sum of the two points.

        TODO: how to handle the IDs better?

        Args:
            other:
                ...

        Returns:
            ret:
                ...

        Example:
            ```py
            >>> point1 = Point(x=3.2, y=-4.6, ID=47)
            >>> point2 = Point(x=-6.4, y=2.5, ID=33)
            >>> result = point1 + point2
            >>> str(result)
            Point(x=-3.2, y=-2.1, ID=80)
            ```
        """

        return Point(x=self._x + other.x, y=self._y + other.y, ID=self._ID + other.ID)

    def __eq__(self, other: IPoint) -> bool:
        """
        This checks to see if two points have the same x- and y-positions (within a
        certain tolerance) regardless of their ID.

        TODO: update this when we can handle other units (e.g., feet, cm, ...)?

        Args:
            other:
                ...

        Returns:
            flag:
                ...

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
        """

        return abs(self._x - other.x) < TOL and abs(self._y - other.y) < TOL

    def __str__(self) -> str:
        """
        This prints the current point instance to the screen.

        Returns:
            ret:
                ...

        Example:
            ```py
            >>> print(point)
            Point(x=3.2, y=-4.6, ID=47)
            ```
        """

        return f"Point(x={self._x}, y={self._y}, ID={self._ID})"

    def __sub__(self, other: IPoint) -> IPoint:
        """
        This subtracts together two points component-wise. This will assign the new
        point an ID corresponding to the sum of the two points.

        TODO: how to handle the IDs better?

        Args:
            other:
                ...

        Returns:
            ret:
                ...

        Example:
            ```py
            >>> point1 = Point(x=3.2, y=-4.6, ID=47)
            >>> point2 = Point(x=-6.4, y=2.5, ID=33)
            >>> result = point1 - point2
            >>> str(result)
            Point(x=9.6, y=-7.1, ID=80)
            ```
        """

        return Point(x=self._x - other.x, y=self._y - other.y, ID=self._ID + other.ID)

    @property
    def ID(self) -> int:
        """
        This gets the ID of the point.

        Type:
            int

        Example:
            ```py
            >>> point = Point(x=3.2, y=-4.6, ID=47)
            >>> point.ID
            47
            ```
        """

        return self._ID

    @property
    def x(self) -> float:
        """
        This gets the x-position of the point.

        Type:
            float

        Example:
            ```py
            >>> point = Point(x=3.2, y=-4.6, ID=47)
            >>> point.x
            3.2
            ```
        """

        return self._x

    @property
    def y(self) -> float:
        """
        This gets the y-position of the point.

        Type:
            float

        Example:
            ```py
            >>> point = Point(x=3.2, y=-4.6, ID=47)
            >>> point.y
            -4.6
            ```
        """

        return self._y


def are_collinear(point1: Point, point2: Point, point3: Point) -> bool:
    """
    This checks to see if three points are collinear. It will do this by computing
    their cross product. If their cross product is zero, then they are collinear. This
    will check this within tolerance.

    Args:
        point1:
            ...
        point2:
            ...
        point3:
            ...

    Returns:
        flag:
            ...
    """

    delta1: Point = point1 - point2
    delta2: Point = point1 - point3
    return abs(cross_product(delta1, delta2)) < TOL


def cross_product(point1: IPoint, point2: IPoint) -> float:
    """
    This computes the z-component of the cross product between the vectors pointing
    from the origin to the each of the two points. If it is positive, then the angle
    between the two vectors is CCW, else it is CW.

    Args:
        point1:
            ...
        point2:
            ...

    Returns:
        ret:
            ...

    Example:
        ```py
        >>> point1 = Point(x=0.5, y=0.5, ID=0)
        >>> point2 = Point(x=-0.5, y=0.5, ID=1)
        >>> cross_product(point1, point2)
        0.5
        >>> cross_product(point2, point1)
        -0.5
        ```
    """

    return point1.x * point2.y - point1.y * point2.x
