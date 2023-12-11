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

    def __str__(self) -> str:
        """
        This prints the node to the screen.

        Returns:
            ret:
                ...

        Example:
            ```py
            >>> node = Node(Point(x=0, y=0, ID=0))
            >>> print(node)
            Node(
                value=Point(x=0, y=0, ID=0),
                left.ID=None,
                right.ID=None,
            )
            >>> node.left = Node(Point(x=1, y=0, ID=-1))
            >>> print(node)
            Node(
                value=Point(x=0, y=0, ID=0),
                left.ID=-1,
                right.ID=None
            )
            >>> node.right = Node(Point(x=-1, y=0, ID=1))
            >>> print(node)
            Node(
                value=Point(x=0, y=0, ID=0),
                left.ID=-1,
                right.ID=1,
            )
            ```
        """

        def output_string(conn: int | None) -> str:
            """This outputs either the connection number as a string or `'None'` as a
            string to be printed."""

            return str(conn.value.ID) if conn is not None else "None"

        ret: str = "Node(\n"
        ret += f"\tvalue={str(self._value)},\n"
        ret += f"\tleft.ID={output_string(self._left)},\n"
        ret += f"\tright.ID={output_string(self._right)},\n"
        return ret + ")"

    @property
    def left(self) -> Node | None:
        """
        This gets the node immediately to the left of this node.

        Type:
            Node | None

        Example:
            ```py
            >>> node = Node(Point(x=0, y=0, ID=0))
            >>> node.left = Node(Point(x=-1, y=0, ID=-1))
            >>> print(node.left.value)
            Point(x=-1, y=0, ID=-1)
            ```
        """

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

        Example:
            ```py
            >>> node = Node(Point(x=0, y=0, ID=0))
            >>> node.left = Node(Point(x=-1, y=0, ID=-1))
            >>> print(node.left.value)
            Point(x=-1, y=0, ID=-1)
            ```
        """

        if self._left is not None:
            raise ValueError("The node to the left has already been set!")

        self._left = node

    @property
    def right(self) -> Node | None:
        """
        This gets the node immediately to the right of this node.

        Type:
            Node | None

        Example:
            ```py
            >>> node = Node(Point(x=0, y=0, ID=0))
            >>> node.right = Node(Point(x=1, y=0, ID=1))
            >>> print(node.right.value)
            Point(x=1, y=0, ID=1)
            ```
        """

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

        Example:
            ```py
            >>> node = Node(Point(x=0, y=0, ID=0))
            >>> node.right = Node(Point(x=1, y=0, ID=1))
            >>> print(node.right.value)
            Point(x=1, y=0, ID=1)
            ```
        """

        if self._right is not None:
            raise ValueError("The node to the right has already been set!")

        self._right = node

    @property
    def value(self) -> IPoint:
        """
        This gets the point wrapped up by the node.

        Type:
            Point

        Example:
            ```py
            >>> node = Node(Point(x=0, y=0, ID=0))
            >>> print(node.value)
            Point(x=0, y=0, ID=0)
            ```
        """

        return self._value

    def del_connection(self, option: NeighborOption) -> None:
        """
        This deletes the connection to a neighboring node.

        Args:
            option:
                Which of the two neighbors to delete.

        Example:
            ```py
            >>> node = Node(Point(x=0, y=0, ID=0))
            >>> node.right = Node(Point(x=1, y=0, ID=1))
            >>> node.right
            <mesher.geometry.ring.Node object at ...>
            >>> node.del_connection(NeighborOption.RIGHT)
            >>> node.right
            ```
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

        Example:
            ```py
            >>> node = Node(Point(x=0, y=0, ID=0))
            >>> node.right = Node(Point(x=1, y=0, ID=1))
            >>> node.right
            <mesher.geometry.ring.Node object at ...>
            >>> node.has_connection(NeighborOption.LEFT)
            False
            >>> node.has_connection(NeighborOption.RIGHT)
            True
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

        Example:
            ```py
            >>> ring = Ring()
            >>> ring.add_point(Point(x=0, y=0, ID=0))
            >>> ring.add_point(Point(x=1, y=0, ID=1))
            >>> ring.add_point(Point(x=1, y=1, ID=2))
            >>> Point(x=1, y=0, ID=3) in ring
            True
            >>> Point(x=0, y=-1, ID=3) in ring
            False
            ```
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

        Example:
            ```py
            >>> ring = Ring()
            >>> ring.add_point(Point(x=0, y=0, ID=0))
            >>> ring.add_point(Point(x=1, y=0, ID=1))
            >>> ring.add_point(Point(x=1, y=1, ID=2))
            >>> str(ring[2])
            Point(x=1, y=1, ID=2)
            ```
        """

        return self._nodes[index].value

    def __iter__(self) -> Iterable[IPoint]:
        """
        This makes the `Ring` into an iterable.

        Yields:
            point:
                ...

        Example:
            ```py
            >>> ring = Ring()
            >>> ring.add_point(Point(x=0, y=0, ID=0))
            >>> ring.add_point(Point(x=1, y=0, ID=1))
            >>> ring.add_point(Point(x=1, y=1, ID=2))
            >>> for point in ring:
            ...     print(point)
            ...
            Point(x=0, y=0, ID=0)
            Point(x=1, y=0, ID=1)
            Point(x=1, y=1, ID=2)
            ```
        """

        for node in self._nodes:
            yield node.value

    def __len__(self) -> int:
        """
        This gets the number of points (nodes) in the ring.

        Returns:
            length:
                ...

        Example:
            ```py
            >>> ring = Ring()
            >>> ring.add_point(Point(x=0, y=0, ID=0))
            >>> ring.add_point(Point(x=1, y=0, ID=1))
            >>> ring.add_point(Point(x=1, y=1, ID=2))
            >>> len(ring)
            3
            ```
        """

        return len(self._nodes)

    def __str__(self) -> str:
        """
        This prints the current ring instance to the screen.

        Returns:
            ret:
                ...

        Example:
            ```py
            >>> ring = Ring()
            >>> ring.add_point(Point(x=0, y=0, ID=0))
            >>> ring.add_point(Point(x=1, y=0, ID=1))
            >>> ring.add_point(Point(x=1, y=1, ID=2))
            >>> print(ring)
            Ring(
                nodes=[
                    Node(
                value=Point(x=0, y=0, ID=0),
                left.ID=None,
                right.ID=None,
                    ),
                    Node(
                value=Point(x=1, y=0, ID=1),
                left.ID=None,
                right.ID=None,
                    ),
                    Node(
                value=Point(x=1, y=1, ID=2),
                left.ID=None,
                right.ID=None,
                    ),
                ]
            )
            ```
        """

        ret: str = "Ring(\n"
        ret += "\tnodes=[\n"
        for node in self._nodes:
            ret += f"\t\t{str(node)},\n"

        return ret + "\t]\n)"

    @property
    def area(self) -> float | None:
        """
        This computes the area enclosed by the closed ring.

        Type:
            float | None

        Example:
            TODO: fill in this example
        """

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
        """
        This checks if the ring is closed.

        Type:
            bool:

        Example:
            TODO: fill in this example
        """

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
        """
        This checks if the ring is convex or concave.

        Type:
            bool | None

        Example:
            TODO: fill in this example
        """

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
        """
        This gets the orientation of the ring.

        Type:
            Orientation | None

        Example:
            TODO: fill in this example
        """

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

        Example:
            ```py
            >>> ring = Ring()
            >>> len(ring)
            0
            >>> ring.add_point(Point(x=0, y=0, ID=0))
            >>> len(ring)
            1
            >>> str(ring[0])
            Point(x=0, y=0, ID=0)
            ```
        """

        if self.closed:
            raise ValueError("You cannot add anymore points! This ring is closed!")

        self._nodes.append(Node(point))

    def close(self) -> None:
        """
        This closes the ring.
        """

        if not self.closed or len(self) > 2:
            for n, node in enumerate(self._nodes):
                n_before: int = n - 1
                n_after: int = (n + 1) % len(self)
                node.left = self._nodes[n_before]
                node.right = self._nodes[n_after]


    def find_point(self, point: IPoint) -> int | None:
        """
        This finds if and where the point is in the ring.

        Args:
            point:
                ...

        Returns:
            index:
                The location of the point (if it is in the ring).

        Example:
            ```py
            >>> ring = Ring()
            >>> ring.add_point(Point(x=0, y=0, ID=0))
            >>> ring.add_point(Point(x=1, y=0, ID=1))
            >>> ring.add_point(Point(x=1, y=1, ID=2))
            >>> ring.find_point(Point(x=1, y=0, ID=4))
            1
            >>> ring.find_point(Point(x=2, y=0, ID=4))
            ```
        """

        for p, pnt in enumerate(self):
            if point == pnt:
                return p

    def find_self_intersections(self) -> list[tuple[int, int, IPoint]]:
        ...

    def insert_point(self, point: IPoint, location: int) -> None:
        """
        This inserts a point into the ring. This will insert the point at the given
        index. If the ring is already closed, then it will delete the connections of
        the nodes before and after this new point and connect themselves to the node.

        Args:
            point:
                ...
            location:
                ...

        Example:
            TODO: fill in this example
        """

        closed: bool = self.closed
        self._nodes.insert(location, Node(point))
        if closed:
            self._nodes[location - 1].del_connection(NeighborOption.RIGHT)
            self._nodes[location - 1].right = self._nodes[location]

            self._nodes[location].left = self._nodes[location - 1]
            self._nodes[location].right = self._nodes[(location + 1) % len(self)]

            self._nodes[(location + 1) % len(self)].del_connection(NeighborOption.LEFT)
            self._nodes[(location + 1) % len(self)].left = self._nodes[location]

    def remove_collinear(self) -> None:
        ...

    def split_ring(self) -> list[IRing]:
        ...
