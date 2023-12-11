from __future__ import annotations

import enum
from typing import Iterable

from .abc import IPoint, IRing
from .point import cross_product


class NeighborOption(enum.Enum):
    """This allows the user to choose between the left or right neighbor."""

    LEFT: int = 0
    """The left neighbor."""

    RIGHT: int = 1
    """The right neighbor."""


class Orientation(enum.Enum):
    """This encodes the orientation of the ring."""

    CCW: int = 0
    """Counter clockwise"""

    CW: int = 1
    "Clockwise"


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


class Ring(IRing):

    """
    This will implement a point-wise curve as a linked-list. This is done in order to
    encode edge information. Each of the [`Point`][mesher.geometry.point.Point] objects
    with a [`Node`][mesh.geometry.ring.Node] instance to encode these links.

    Attributes:
        area:           The area enclosed by the (closed) ring.
        closed:         This checks if the ring is the ring closed.
        is_convex:      This checks if the ring is the ring convex of concave.
        nodes:          The list of nodes defining the ring.
        orientation:    This checks if the ring is CCW or CW.
    """

    def __init__(self) -> None:
        """Constructor..."""

        self._nodes: list[Node] = []
        """
        The list of nodes defining the ring.

        Type:
            list[Node]
        """

    def __contains__(self, point: IPoint) -> bool:
        """
        This checks if a point is in a ring.

        Args:
            point:
                ...

        Returns:
            flag:
                ...
        """

        for node in self._nodes:
            if point == node.value:
                return True

        return False

    def __eq__(self, other: IRing) -> bool:
        ...

    def __getitem__(self, index: int) -> IPoint:
        """
        This gets the point (node) at the given index.

        Args:
            index:
                ...

        Returns:
            ret:
                ...
        """

        return self._nodes[index].value

    def __iter__(self) -> Iterable[IPoint]:
        """
        This makes the `Ring` into an iterable.

        Yields:
            point:
                ...
        """

        for node in self._nodes:
            yield node.value

    def __len__(self) -> int:
        """
        This gets the number of points (nodes) in the ring.

        Returns:
            length:
                ...
        """

        return len(self._nodes)

    def __str__(self) -> str:
        """
        This prints the current ring instance to the screen.

        Returns:
            ret:
                ...
        """

        ret: str = "Ring(\n"
        ret += "\tpoints=[\n"
        for node in self._nodes:
            ret += f"\t\t{str(node.value)},\n"

        return ret + "\t]\n)"

    @property
    def area(self) -> float | None:
        """This computes the area enclosed by the closed ring."""

        if not self.closed:
            return None

        ret: float = 0
        for n in range(len(self._nodes)):
            n1: int = n
            n2: int = (n + 1) % len(self._nodes)

            p1: IPoint = self._nodes[n1].value
            p2: IPoint = self._nodes[n2].value

            ret += cross_product(p1, p2)

        return ret * 0.5

    @property
    def closed(self) -> bool:
        """This checks if the ring is closed."""

        if len(self._nodes) <= 2:
            return False

        for node in self._nodes:
            if not node.has_connection(NeighborOption.LEFT) or not node.has_connection(
                NeighborOption.RIGHT
            ):
                return False

        return True

    @property
    def is_convex(self) -> bool | None:
        """This checks if the ring is convex or concave."""

        if not self.closed:
            return None

        is_CCW: list[bool] = []
        for n in range(len(self._nodes)):
            n1: int = n
            n2: int = (n + 1) % len(self._nodes)
            n3: int = (n + 2) % len(self._nodes)

            delta1: IPoint = self._nodes[n1].value - self._nodes[n2].value
            delta2: IPoint = self._nodes[n1].value - self._nodes[n3].value
            is_CCW.append(cross_product(delta1, delta2) > 0)

        if all(is_CCW) or all(not flag for flag in is_CCW):
            return True
        else:
            return False

    @property
    def orientation(self) -> Orientation | None:
        """This gets the orientation of the ring."""

        if not self.closed:
            return None

        if self.area > 0:
            return Orientation.CCW
        elif self.area < 0:
            return Orientation.CW

    def add_point(self, point: IPoint) -> None:
        """
        This adds a point to the ring if the ring is not closed.

        Args:
            point:
                ...

        Raises:
            ValueError:
                You cannot add anymore points! This ring is closed!
        """

        if self.closed:
            raise ValueError("You cannot add anymore points! This ring is closed!")
        
        self._nodes.append(Node(point))

    def close(self) -> None:
        ...

    def find_point(self, point: IPoint) -> int | None:
        """
        This finds if and where the point is in the ring.

        Args:
            point:
                ...

        Returns:
            index:
                The location of the point (if it is in the ring).
        """

        for p, pnt in enumerate(self):
            if point == pnt:
                return p

    def find_self_intersections(self) -> list[tuple[int, int, IPoint]]:
        ...

    def insert_point(self, point: IPoint, location: int) -> None:
        ...

    def remove_collinear(self) -> None:
        ...

    def split_ring(self) -> list[IRing]:
        ...
