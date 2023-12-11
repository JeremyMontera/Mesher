import pytest

from mesher.geometry.ring import Node, Ring
from mesher.geometry.point import Point


@pytest.fixture
def sample_points() -> dict[str, list[Point]]:
    """Generates sample points from a number of scenarios for testing."""

    # TODO: handle open rings, self-intersecting rings

    return {
        "closed,CCW,convex": [
            Point(x=0, y=0, ID=0),
            Point(x=1, y=0, ID=1),
            Point(x=1, y=2, ID=2),
            Point(x=0, y=2, ID=3),
        ],
        "closed,CW,convex": [
            Point(x=0, y=0, ID=0),
            Point(x=0, y=2, ID=1),
            Point(x=1, y=2, ID=2),
            Point(x=1, y=0, ID=3),
        ],
        "closed,CCW,concave": [
            Point(x=0, y=0, ID=0),
            Point(x=2, y=2, ID=1),
            Point(x=0, y=1, ID=2),
            Point(x=-2, y=2, ID=3),
        ],
        "closed,CW,concave": [
            Point(x=0, y=0, ID=0),
            Point(x=-2, y=2, ID=1),
            Point(x=0, y=1, ID=2),
            Point(x=2, y=2, ID=3),
        ],
    }


@pytest.fixture
def sample_rings(sample_points: dict[str, list[Point]]) -> dict[str, Ring]:
    """Generates sample rings for testing."""

    rings: dict[str, Ring] = {}
    for scenario, points in sample_points.items():
        ring: Ring = Ring()
        ring._nodes: list[Node] = [Node(point) for point in points]
        rings[scenario] = ring

    return rings


def test_ring_init(sample_rings):
    """Tests ring constructor."""

    for _, ring in sample_rings.items():
        assert hasattr(ring, "_nodes")
        assert isinstance(ring._nodes, list)
        assert len(ring._nodes) == 4


def test_ring_contains(sample_rings):
    """This tests ring contains operator."""

    point1: Point = Point(x=1, y=2, ID=4)
    point2: Point = Point(x=2, y=1, ID=5)

    assert point1 in sample_rings["closed,CCW,convex"]
    assert point2 not in sample_rings["closed,CCW,convex"]


def test_ring_getitem(sample_rings, sample_points):
    """This tests ring getitem operator."""

    for scenario, ring in sample_rings.items():
        for p, point in enumerate(sample_points[scenario]):
            assert ring[p] == point


def test_ring_iter(sample_rings, sample_points):
    """This tests ring iterator."""

    for scenario, ring in sample_rings.items():
        for p, point in enumerate(ring):
            assert point == sample_points[scenario][p]


def test_ring_len(sample_rings, sample_points):
    """This tests ring length."""

    for scenario, ring in sample_rings.items():
        assert len(ring) == len(sample_points[scenario])


def test_ring_str(sample_rings, sample_points):
    """This tests that the ring is properly printed to the screen."""

    for scenario, ring in sample_rings.items():
        ret: str = "Ring(\n\tpoints=[\n"
        for point in sample_points[scenario]:
            ret += f"\t\t{str(point)},\n"

        ret += "\t]\n)"

        assert str(ring) == ret


@pytest.mark.parametrize(
    "scenario,result",
    [
        ("closed,CCW,convex", 2.0),
        ("closed,CW,convex", -2.0),
        ("closed,CCW,concave", 2.0),
        ("closed,CW,concave", -2.0),
    ]
)
def test_ring_area(sample_rings, scenario, result):
    """This tests that the area of a ring is properly computed."""

    assert sample_rings[scenario].area == result

# def test_ring_is_convex(sample_ring):
#     """This tests that the concavity of a closed ring is computed correctly."""
    
#     ...
