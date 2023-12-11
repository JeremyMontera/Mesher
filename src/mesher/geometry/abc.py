from __future__ import annotations

import abc
from typing import Iterable, Literal


class IPoint(metaclass=abc.ABCMeta):

    """This is the interface for the [`Point`][mesher.geometry.point.Point] class."""

    @abc.abstractmethod
    def __init__(self, *, x: float, y: float, ID: int) -> None:
        """Constructor..."""

        ...

    @abc.abstractmethod
    def __add__(self, other: IPoint) -> IPoint:
        """This adds together two points component-wise."""

        ...

    @abc.abstractmethod
    def __eq__(self, other: IPoint) -> bool:
        """This checks to see if two points have the same x- and y-positions (within a
        certain tolerance) regardless of their ID."""

        ...

    @abc.abstractmethod
    def __sub__(self, other: IPoint) -> IPoint:
        """This subtracts together two points component-wise."""

        ...

    @abc.abstractmethod
    def __str__(self) -> str:
        """This prints the current point instance to the screen."""

        ...

    @property
    @abc.abstractmethod
    def ID(self) -> int:
        """This gets the ID of the point."""

        ...

    @property
    @abc.abstractmethod
    def x(self) -> float:
        """This gets the x-position of the point."""

        ...

    @property
    @abc.abstractmethod
    def y(self) -> float:
        """This gets the y-position of the point."""

        ...


class IRing(metaclass=abc.ABCMeta):

    """This is the interface for the [`Ring`][mesher.geometry.ring.Ring] class."""

    @abc.abstractmethod
    def __init__(self) -> None:
        """Constructor..."""

        ...

    @abc.abstractmethod
    def __contains__(self, point: IPoint) -> bool:
        """This checks if a point is in a ring."""

        ...

    @abc.abstractmethod
    def __eq__(self, other: IRing) -> bool:
        """This checks if two rings are equal within tolerance."""

        ...

    @abc.abstractmethod
    def __getitem__(self, index: int) -> IPoint:
        """This gets the point (node) at the given index."""

        ...

    @abc.abstractmethod
    def __iter__(self) -> Iterable[IPoint]:
        """This makes the `Ring` into an iterable."""

        ...

    @abc.abstractmethod
    def __len__(self) -> int:
        """This gets the number of points (nodes) in the ring."""

        ...

    @abc.abstractmethod
    def __str__(self) -> str:
        """This prints the current ring instance to the screen."""

        ...

    @property
    @abc.abstractmethod
    def area(self) -> float | None:
        """This computes the area enclosed by the closed ring."""

        ...

    @property
    @abc.abstractmethod
    def closed(self) -> bool:
        """This checks if the ring is closed."""

        ...

    @property
    @abc.abstractmethod
    def is_convex(self) -> bool | None:
        """This checks if the ring is convex or concave."""

        ...

    @property
    @abc.abstractmethod
    def orientation(self) -> Literal | None:
        """This gets the orientation of the ring."""

        ...

    @abc.abstractmethod
    def add_point(self, point: IPoint) -> None:
        """This adds a point to the ring if the ring is not closed."""

        ...

    @abc.abstractmethod
    def close(self) -> None:
        """This closes the ring."""

        ...

    @abc.abstractmethod
    def find_point(self, point: IPoint) -> int | None:
        """This finds if and where the point is in the ring."""

        ...

    @abc.abstractmethod
    def find_self_intersections(self) -> list[tuple[int, int, IPoint]]:
        """This finds if and where the ring has any self-intersections."""

        ...

    @abc.abstractmethod
    def insert_point(self, point: IPoint, location: int) -> None:
        """This inserts a point into the ring."""

        ...

    @abc.abstractmethod
    def remove_collinear(self) -> None:
        """This removes any collinear points (nodes)."""

        ...

    @abc.abstractmethod
    def split_ring(self) -> list[IRing]:
        """This splits a ring that has self-intersections into multiple,
        non-self-intersecting rings."""

        ...
