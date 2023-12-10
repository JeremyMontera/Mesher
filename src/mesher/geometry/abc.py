from __future__ import annotations

import abc


class IPoint(metaclass=abc.ABCMeta):

    """This is the interface for the [`Point`][mesher.geometry.point.Point] class."""

    @abc.abstractmethod
    def __init__(self, *, x: float, y: float, ID: int) -> None:
        """Constructor..."""

        ...

    @abc.abstractmethod
    def __eq__(self, other: IPoint) -> bool:
        """This checks to see if two points have the same x- and y-positions (within a
        certain tolerance) regardless of their ID."""

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
