import pytest

from mesher.geometry.ring import Node, Ring
from mesher.geometry.point import Point


@pytest.fixture
def sample_points() -> list[Point]:
    """Generates sample points for testing."""

    return [
        Point(x=0, y=0, ID=0),
        Point(x=1, y=0, ID=1),
        Point(x=1, y=2, ID=2),
        Point(x=0, y=2, ID=3),
    ]


@pytest.fixture
def sample_ring(sample_points):
    """Generates a sample ring for testing."""

    ring: Ring = Ring()
    ring._nodes: list[Node] = [Node(point) for point in sample_points]
    return ring


def test_ring_init(sample_ring):
    """Tests ring constructor."""

    assert hasattr(sample_ring, "_nodes")
    assert isinstance(sample_ring._nodes, list)
    assert len(sample_ring._nodes) == 4


def test_ring_contains(sample_ring):
    """This tests ring contains operator."""

    point1: Point = Point(x=1, y=2, ID=4)
    point2: Point = Point(x=2, y=1, ID=5)

    assert point1 in sample_ring
    assert point2 not in sample_ring


def test_ring_getitem(sample_ring, sample_points):
    """This tests ring getitem operator."""

    for p, point in enumerate(sample_points):
        assert sample_ring[p] == point


def test_ring_iter(sample_ring, sample_points):
    """This tests ring iterator."""

    for p, point in enumerate(sample_ring):
        assert point == sample_points[p]


def test_ring_len(sample_ring, sample_points):
    """This tests ring length."""

    assert len(sample_ring) == len(sample_points)


def test_ring_str(sample_ring, sample_points):
    """This tests that the ring is properly printed to the screen."""

    ret: str = "Ring(\n\tpoints=[\n"
    for point in sample_points:
        ret += f"\t\t{str(point)},\n"

    ret += "\t]\n)"

    assert str(sample_ring) == ret


def test_ring_area(sample_ring):
    """This tests that the area of a ring is properly computed."""

    assert sample_ring.area == 2.0

def test_ring_is_convex(sample_ring):
    """This tests that the concavity of a closed ring is computed correctly."""
    
    ...
