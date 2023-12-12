from __future__ import annotations

import enum
from typing import Iterable

from .abc import IPoint, IRing
from .point import are_collinear, cross_product


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
        """
        This checks if two rings are equal within tolerance. This will first check that
        the number of points are equal, and that all the points line up by checking
        that (a) the points are equal, and (b) the ordering of the points is equal.

        Args:
            other:
                ...

        Returns:
            flag:
                ...

        Example:
            ```py
            >>> ring1 = Ring()
            >>> ring1.add_point(Point(x=0, y=0, ID=0))
            >>> ring1.add_point(Point(x=1, y=1, ID=1))
            >>> ring1.add_point(Point(x=0, y=2, ID=2))
            >>> ring1.close()
            >>> ring2 = Ring()
            >>> ring2.add_point(Point(x=0, y=0, ID=3))
            >>> ring2.add_point(Point(x=1, y=1, ID=4))
            >>> ring2.add_point(Point(x=0, y=2, ID=5))
            >>> ring2.close()
            >>> ring1 == ring2
            True
            ```
        """

        if len(self) != len(other):
            return False
        
        if self[0] not in other:
            return False
        
        ptr0: int = other.find_point(self[0]) + 1
        ptr1: int = 1
        while True:
            if self[ptr0] != other[ptr1]:
                return False
            
            if (
                self._nodes[ptr0].left.value != other._nodes[ptr1].left.value or
                self._nodes[ptr0].right.value != other._nodes[ptr1].right.value
            ):
                return False
            
            ptr0: int = (ptr0 + 1) % len(self)
            ptr1: int = (ptr1 + 1) % len(other)
            if ptr1 == 0:
                break

        return True

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
            ```py
            >>> ring = Ring()
            >>> ring.add_point(Point(x=0, y=0, ID=0))
            >>> ring.add_point(Point(x=1, y=0, ID=1))
            >>> ring.add_point(Point(x=1, y=1, ID=2))
            >>> ring.close()
            >>> ring.area
            0.5
            ```
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
            ```py
            >>> ring = Ring()
            >>> ring.add_point(Point(x=0, y=0, ID=0))
            >>> ring.add_point(Point(x=1, y=0, ID=1))
            >>> ring.add_point(Point(x=1, y=1, ID=2))
            >>> ring.closed
            False
            >>> ring.close()
            >>> ring.closed
            True
            ```
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
            ```py
            >>> ring = Ring()
            >>> ring.add_point(Point(x=0, y=0, ID=0))
            >>> ring.add_point(Point(x=2, y=2, ID=1))
            >>> ring.add_point(Point(x=0, y=1, ID=2))
            >>> ring.add_point(Pointx=-2, y=2, ID=3))
            >>> ring.close()
            >>> ring.is_convex
            True
            ```
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
            ```py
            >>> ring = Ring()
            >>> ring.add_point(Point(x=0, y=0, ID=0))
            >>> ring.add_point(Point(x=1, y=0, ID=1))
            >>> ring.add_point(Point(x=1, y=1, ID=2))
            >>> ring.orientation
            <Orientation.CCW: 0>
            ```
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

        Example:
            ```py
            >>> ring = Ring()
            >>> ring.add_point(Point(x=0, y=0, ID=0))
            >>> ring.add_point(Point(x=1, y=0, ID=1))
            >>> ring.add_point(Point(x=1, y=1, ID=2))
            >>> ring.closed
            False
            >>> ring.close()
            >>> ring.closed
            True
            ```
        """

        if not self.closed or len(self) > 2:
            for n, node in enumerate(self._nodes):
                n_before: int = n - 1
                n_after: int = (n + 1) % len(self)
                node.left = self._nodes[n_before]
                node.right = self._nodes[n_after]

    def delete_point(self, location: int) -> None:
        """
        This deletes a point from a ring whether open or closed. It will also update
        the connections for a closed ring - the nodes to the left and right of the
        deleted node will be connected to each other.

        Args:
            location:
                ...

        Example:
            ```py
            >>> ring = Ring()
            >>> ring.add_point(Point(x=0, y=0, ID=0))
            >>> ring.add_point(Point(x=1, y=0, ID=1))
            >>> ring.add_point(Point(x=2, y=0, ID=2))
            >>> ring.add_point(Point(x=1, y=2, ID=3))
            >>> ring.close()
            >>> print(ring)
            Ring(
                nodes=[
                    Node(
                value=Point(x=0, y=0, ID=0),
                left.ID=3,
                right.ID=1,
                    ),
                    Node(
                value=Point(x=1, y=0, ID=1),
                left.ID=0,
                right.ID=2,
                    ),
                    Node(
                value=Point(x=2, y=0, ID=2),
                left.ID=1,
                right.ID=3,
                    ),
                    Node(
                value=Point(x=1, y=2, ID=3),
                left.ID=2,
                right.ID=0,
                    ),
                ]
            )
            >>> ring.delete_point(1)
            >>> print(ring)
            Ring(
                nodes=[
                    Node(
                value=Point(x=0, y=0, ID=0),
                left.ID=3,
                right.ID=2,
                    ),
                    Node(
                value=Point(x=2, y=0, ID=2),
                left.ID=0,
                right.ID=3,
                    ),
                    Node(
                value=Point(x=1, y=2, ID=3),
                left.ID=2,
                right.ID=0,
                    ),
                ]
            )
            ```
        """

        if self.closed:
            before: int = location - 1
            after: int = (location + 1) % len(self)

            self._nodes[before].del_connection(NeighborOption.RIGHT)
            self._nodes[after].del_connection(NeighborOption.LEFT)

            self._nodes[before].right = self._nodes[after]
            self._nodes[after].left = self._nodes[before]

        del self._nodes[location]

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
            ```py
            >>> ring = Ring()
            >>> ring.add_point(Point(x=0, y=0, ID=0))
            >>> ring.add_point(Point(x=1, y=0, ID=1))
            >>> ring.add_point(Point(x=1, y=1, ID=2))
            >>> ring.close()
            >>> print(ring)
            Ring(
                nodes=[
                    Node(
                value=Point(x=0, y=0, ID=0),
                left.ID=2,
                right.ID=1,
                    ),
                    Node(
                value=Point(x=1, y=0, ID=1),
                left.ID=0,
                right.ID=2,
                    ),
                    Node(
                value=Point(x=1, y=1, ID=2),
                left.ID=1,
                right.ID=0,
                    ),
                ]
            )
            >>> ring.insert_point(Point(x=0.5, y=2, ID=3), 3)
            >>> print(ring)
            Ring(
                nodes=[
                    Node(
                value=Point(x=0, y=0, ID=0),
                left.ID=3,
                right.ID=1,
                    ),
                    Node(
                value=Point(x=1, y=0, ID=1),
                left.ID=0,
                right.ID=2,
                    ),
                    Node(
                value=Point(x=1, y=1, ID=2),
                left.ID=1,
                right.ID=3,
                    ),
                    Node(
                value=Point(x=0.5, y=2, ID=3),
                left.ID=2,
                right.ID=0,
                    )
                ]
            )
            ```
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
        """
        This removes any collinear points (nodes).

        Example:
            ```py
            >>> ring = Ring()
            >>> ring.add_point(Point(x=0, y=0, ID=0))
            >>> ring.add_point(Point(x=1, y=0, ID=1))
            >>> ring.add_point(Point(x=2, y=0, ID=2))
            >>> ring.add_point(Point(x=1, y=2, ID=3))
            >>> ring.close()
            >>> print(ring)
            Ring(
                nodes=[
                    Node(
                value=Point(x=0, y=0, ID=0),
                left.ID=3,
                right.ID=1,
                    ),
                    Node(
                value=Point(x=1, y=0, ID=1),
                left.ID=0,
                right.ID=2,
                    ),
                    Node(
                value=Point(x=2, y=0, ID=2),
                left.ID=1,
                right.ID=3,
                    ),
                    Node(
                value=Point(x=1, y=2, ID=3),
                left.ID=2,
                right.ID=0,
                    ),
                ]
            )
            >>> ring.remove_collinear()
            >>> print(ring)
            Ring(
                nodes=[
                    Node(
                value=Point(x=0, y=0, ID=0),
                left.ID=3,
                right.ID=2,
                    ),
                    Node(
                value=Point(x=2, y=0, ID=2),
                left.ID=0,
                right.ID=3,
                    ),
                    Node(
                value=Point(x=1, y=2, ID=3),
                left.ID=2,
                right.ID=0,
                    ),
                ]
            )
            ```
        """

        idxs: list[int] = list(range(len(self)))
        for i in range(len(self) - 1):
            n1: int = idxs[i % len(idxs)]
            n2: int = idxs[(i + 1) % len(idxs)]
            n3: int = idxs[(i + 2) % len(idxs)]
            if are_collinear(self[n1], self[n2], self[n3]):
                del idxs[i + 1]

        self._nodes: list[Node] = [self._nodes[idx] for idx in idxs]
        for n, node in enumerate(self._nodes):
            n_before: int = n - 1
            n_after: int = (n + 1) % len(self._nodes)

            node.del_connection(NeighborOption.LEFT)
            node.del_connection(NeighborOption.RIGHT)

            node.left = self._nodes[n_before]
            node.right = self._nodes[n_after]

    def reverse_orientation(self) -> None:
        """
        This reversed the orientation of a closed ring. This will also swap the left
        and right connections of each node.

        Example:
            ```py
            >>> ring = Ring()
            >>> ring.add_point(Point(x=0, y=0, ID=0))
            >>> ring.add_point(Point(x=1, y=0, ID=1))
            >>> ring.add_point(Point(x=1, y=1, ID=2))
            >>> ring.close()
            >>> print(ring)
            Ring(
                nodes=[
                    Node(
                value=Point(x=0, y=0, ID=0),
                left.ID=2,
                right.ID=1,
                    ),
                    Node(
                value=Point(x=1, y=0, ID=1),
                left.ID=0,
                right.ID=2,
                    ),
                    Node(
                value=Point(x=1, y=1, ID=2),
                left.ID=1,
                right.ID=0,
                    ),
                ]
            )
            >>> ring.reverse_orientation()
            >>> print(ring)
            Ring(
                nodes=[
                    Node(
                value=Point(x=1, y=1, ID=2),
                left.ID=0,
                right.ID=1,
                    ),
                    Node(
                value=Point(x=1, y=0, ID=1),
                left.ID=2,
                right.ID=0,
                    ),
                    Node(
                value=Point(x=0, y=0, ID=0),
                left.ID=1,
                right.ID=2,
                    ),
                ]
            )
            ```
        """

        if self.closed:
            self._nodes.reverse()
            for node in self._nodes:
                left, right = node.left, node.right
                node.del_connection(NeighborOption.LEFT)
                node.del_connection(NeighborOption.RIGHT)
                node.left, node.right = right, left

    def split_ring(self) -> list[IRing]:
        ...
