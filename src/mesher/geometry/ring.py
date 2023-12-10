from __future__ import annotations

import enum

from .abc import IPoint


class NeighborOption(enum.Enum):
    """This allows the user to choose between the left or right neighbor."""

    LEFT: int = 0
    """The left neighbor."""

    RIGHT: int = 1
    """The right neighbor."""


class Node:

    """
    This will implement a wrapper that encapsulates
    [`Point`][mesher.geometry.point.Point] objects when added as elements to a `Ring`.
    This will have two nodes, thus making a `Ring` a linked list. This will
    automatically handle edges.

    Attributes:
        left:   The node immediately to the left of this node.
        right:  The node immediately to the right of this node.
        value:  The point wrapped up by this node.
    """

    def __init__(self, value: IPoint) -> None:
        """
        Constructor...

        Args:
            value:
                The point wrapped up by this node.
        """

        self._left: Node | None = None
        """
        The node immediately to the left of this node.

        Type:
            Node
        """

        self._right: Node | None = None
        """
        The node immediately to the right of this node.

        Type:
            Node
        """

        self._value: IPoint = value
        """
        The point wrapped up by this node.

        Type:
            Point
        """

    @property
    def left(self) -> Node:
        """This gets the node immediately to the left of this node."""

        return self._left

    @left.setter
    def left(self, node: Node) -> None:
        """
        This sets the node immediately to the left of this node.

        Args:
            node:
                ...

        Raises:
            ValueError:
                The node to the left has already been set!
        """

        if self._left is not None:
            raise ValueError("The node to the left has already been set!")

        self._left = node

    @property
    def right(self) -> Node:
        """This gets the node immediately to the right of this node."""

        return self._right

    @right.setter
    def right(self, node: Node) -> None:
        """
        This sets the node immediately to the right of this node.

        Args:
            node:
                ...

        Raises:
            ValueError:
                The node to the right has already been set!
        """

        if self._right is not None:
            raise ValueError("The node to the right has already been set!")

        self._right = node

    @property
    def value(self) -> IPoint:
        """This gets the point wrapped up by the node."""

        return self._value

    def del_connection(self, option: NeighborOption) -> None:
        """
        This deletes the connection to a neighboring node.

        Args:
            option:
                Which of the two neighbors to delete.
        """

        if option == NeighborOption.LEFT:
            self._left = None
        elif option == NeighborOption.RIGHT:
            self._right = None

    def has_connection(self, option: NeighborOption) -> bool:
        """
        This checks if the neighboring node is already set.

        Args:
            option:
                Which of the two neighbors to check.

        Returns:
            flag:
                ...
        """

        if option == NeighborOption.LEFT:
            return self._left is not None
        elif option == NeighborOption.RIGHT:
            return self._right is not None
