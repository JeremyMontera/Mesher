import pytest

from mesher.geometry.point import Point
from mesher.geometry.ring import NeighborOption, Node

@pytest.fixture
def sample_data() -> list[int, Point]:
    """Generate sample points."""

    return [
        Point(x=-0.02, y=0.03, ID=0),
        Point(x=-0.04, y=0.06, ID=1),
        Point(x=-0.06, y=0.09, ID=2),
    ]

@pytest.fixture
def sample_nodes(sample_data) -> list[Node]:
    """Generate sample nodes."""

    return [Node(point) for point in sample_data]

def test_node_init(sample_nodes, sample_data):
    """Tests node construction."""

    for node, point in zip(sample_nodes, sample_data):
        assert hasattr(node, "_left")
        assert hasattr(node, "_right")
        assert hasattr(node, "_value")
        assert node._left is None
        assert node._right is None
        assert node._value == point

def test_node_neighbor_setter_error():
    """Tests that neighbor setter raises an error."""

    node: Node = Node(Point(x=0, y=0, ID=0))
    node._left = Node(Point(x=0, y=1, ID=1))
    node._right = Node(Point(x=1, y=0, ID=2))
    with pytest.raises(ValueError) as exc:
        node.left = Node(Point(x=1, y=1, ID=3))

    assert exc.value.args[0] == "The node to the left has already been set!"
    with pytest.raises(ValueError) as exc:
        node.right = Node(Point(x=0, y=0, ID=4))

    assert exc.value.args[0] == "The node to the right has already been set!"

def test_node_neighbor_setter(sample_nodes):
    """Tests neighbor setter."""

    for n, node in enumerate(sample_nodes):
        n_before: int = n - 1
        n_after: int = (n + 1) % len(sample_nodes)
        node.left = sample_nodes[n_before]
        node.right = sample_nodes[n_after]

        assert node._left.value.ID == sample_nodes[n_before].value.ID
        assert node._right.value.ID == sample_nodes[n_after].value.ID

def test_node_neighbor_getter(sample_nodes):
    """Tests neighbor getter."""

    for n, node in enumerate(sample_nodes):
        n_before: int = n - 1
        n_after: int = (n + 1) % len(sample_nodes)
        node._left = sample_nodes[n_before]
        node._right = sample_nodes[n_after]

        assert node.left.value.ID == sample_nodes[n_before].value.ID
        assert node.right.value.ID == sample_nodes[n_after].value.ID

def test_node_neighbor_del_connection(sample_nodes):
    """Tests neighbor deleter."""

    for n, node in enumerate(sample_nodes):
        n_before: int = n - 1
        n_after: int = (n + 1) % len(sample_nodes)
        node._left = sample_nodes[n_before]
        node._right = sample_nodes[n_after]

        assert node._left is not None
        assert node._right is not None

        node.del_connection(NeighborOption.LEFT)
        node.del_connection(NeighborOption.RIGHT)

        assert node._left is None
        assert node._right is None

def test_node_has_connection(sample_nodes):
    """Tests neighbor connections status."""

    for n, node in enumerate(sample_nodes):
        n_before: int = n - 1
        n_after: int = (n + 1) % len(sample_nodes)

        assert not node.has_connection(NeighborOption.LEFT)
        assert not node.has_connection(NeighborOption.RIGHT)

        node._left = sample_nodes[n_before]
        node._right = sample_nodes[n_after]

        assert node.has_connection(NeighborOption.LEFT)
        assert node.has_connection(NeighborOption.RIGHT)