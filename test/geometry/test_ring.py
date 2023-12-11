import pytest

from mesher.geometry.point import Point
from mesher.geometry.ring import Node, Orientation, Ring


@pytest.fixture
def sample_points() -> dict[str, list[Point]]:
    """Generates sample points from a number of scenarios for testing."""

    # TODO: handle self-intersecting rings

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
        "open,len=2": [
            Point(x=0, y=0, ID=0),
            Point(x=0, y=1, ID=1),
        ],
        "open,len>2": [
            Point(x=0, y=0, ID=0),
            Point(x=1, y=0, ID=1),
            Point(x=0, y=1, ID=2),
        ],
    }


@pytest.fixture
def sample_rings(sample_points: dict[str, list[Point]]) -> dict[str, Ring]:
    """Generates sample rings for testing."""

    rings: dict[str, Ring] = {}
    for scenario, points in sample_points.items():
        ring: Ring = Ring()
        ring._nodes: list[Node] = [Node(point) for point in points]
        if "closed" in scenario:
            for n in range(len(ring._nodes)):
                n_before: int = n - 1
                n_after: int = (n + 1) % len(ring._nodes)
                ring._nodes[n].left = ring._nodes[n_before]
                ring._nodes[n].right = ring._nodes[n_after]

        rings[scenario] = ring

    return rings


def test_ring_init(sample_rings, sample_points):
    """Tests ring constructor."""

    for scenario, ring in sample_rings.items():
        assert hasattr(ring, "_nodes")
        assert isinstance(ring._nodes, list)
        assert len(ring._nodes) == len(sample_points[scenario])


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
        print(f"{scenario=}")
        ret: str = "Ring(\n\tnodes=[\n"
        for n, point in enumerate(sample_points[scenario]):
            if "closed" in scenario:
                n_before: int = n - 1
                n_after: int = (n + 1) % len(sample_points[scenario])
                node: Node = Node(point)
                node.left = Node(sample_points[scenario][n_before])
                node.right = Node(sample_points[scenario][n_after])
            elif "open" in scenario:
                node: Node = Node(point)

            ret += f"\t\t{str(node)},\n"

        ret += "\t]\n)"

        print(ring)
        print(ret)

        assert str(ring) == ret


@pytest.mark.parametrize(
    "scenario,result",
    [
        ("closed,CCW,convex", 2.0),
        ("closed,CW,convex", -2.0),
        ("closed,CCW,concave", 2.0),
        ("closed,CW,concave", -2.0),
        ("open,len=2", None),
        ("open,len>2", None),
    ],
)
def test_ring_area(sample_rings, scenario, result):
    """This tests that the area of a ring is properly computed."""

    if "closed" in scenario:
        assert sample_rings[scenario].area == result
    elif "open" in scenario:
        assert sample_rings[scenario].area is None


@pytest.mark.parametrize(
    "scenario,flag",
    [
        ("closed,CCW,convex", True),
        ("closed,CW,convex", True),
        ("closed,CCW,concave", True),
        ("closed,CW,concave", True),
        ("open,len=2", False),
        ("open,len>2", False),
    ],
)
def test_ring_closed(sample_rings, scenario, flag):
    """This tests that the ring is closed or not."""

    if flag:
        assert sample_rings[scenario].closed
    else:
        assert not sample_rings[scenario].closed


@pytest.mark.parametrize(
    "scenario,result",
    [
        ("closed,CCW,convex", True),
        ("closed,CW,convex", True),
        ("closed,CCW,concave", False),
        ("closed,CW,concave", False),
        ("open,len=2", None),
        ("open,len>2", None),
    ],
)
def test_ring_is_convex(sample_rings, scenario, result):
    """This tests that the concavity of a closed ring is computed correctly."""

    if "closed" in scenario:
        if result:
            assert sample_rings[scenario].is_convex
        else:
            assert not sample_rings[scenario].is_convex
    elif "open" in scenario:
        assert sample_rings[scenario].is_convex is None


@pytest.mark.parametrize(
    "scenario",
    [
        ("closed,CCW,convex",),
        ("closed,CW,convex",),
        ("closed,CCW,concave",),
        ("closed,CW,concave",),
        ("open,len=2",),
        ("open,len>2",),
    ],
)
def test_ring_orientation(sample_rings, scenario):
    """This tests that the orientation of a closed ring is computed correctly."""

    if "closed" in scenario and "CCW" in scenario:
        assert sample_rings[scenario].orientation == Orientation.CCW
    elif "closed" in scenario and "CW" in scenario:
        assert sample_rings[scenario].orientation == Orientation.CW
    elif "open" in scenario:
        assert sample_rings[scenario].orientation is None


def test_ring_add_point_error_ring_closed(sample_rings):
    """This tests that an error is raised when trying to add point to a closed ring."""

    with pytest.raises(ValueError) as exc:
        sample_rings["closed,CCW,convex"].add_point(Point(x=0, y=-1, ID=10))

    assert exc.value.args[0] == "You cannot add anymore points! This ring is closed!"


def test_ring_add_point(sample_rings, sample_points):
    """This tests adding a point to an open ring."""

    for scenario, ring in sample_rings.items():
        if "open" in scenario:
            ring.add_point(Point(x=-1, y=-1, ID=10))

            assert len(ring._nodes) == len(sample_points[scenario]) + 1
            assert ring._nodes[-1].value == Point(x=-1, y=-1, ID=10)


def test_ring_close(sample_rings, sample_points):
    """This tests closing open rings."""

    ring: Ring = sample_rings["open,len>2"]
    ring.close()
    for n, node in enumerate(ring._nodes):
        n_before: int = n - 1
        n_after: int = (n + 1) % len(ring._nodes)

        node.left.value.ID == sample_points["open,len>2"][n_before].ID
        node.right.value.ID == sample_points["open,len>2"][n_after].ID


@pytest.mark.parametrize(
    "scenario,point,loc",
    [
        ("closed,CCW,convex", Point(x=0, y=1, ID=-1), None),
        ("closed,CW,convex", Point(x=0, y=1, ID=-1), None),
        ("closed,CCW,concave", Point(x=0, y=1, ID=-1), 2),
        ("closed,CW,concave", Point(x=0, y=1, ID=-1), 2),
        ("open,len=2", Point(x=0, y=1, ID=-1), 1),
        ("open,len>2", Point(x=0, y=1, ID=-1), 2),
    ],
)
def test_ring_find_point(sample_rings, scenario, point, loc):
    """This tests finding a point in a ring."""

    if loc is not None:
        assert sample_rings[scenario].find_point(point) == loc
    else:
        assert sample_rings[scenario].find_point(point) is None


def test_ring_insert_point_open(sample_rings, sample_points):
    """This tests inserting a new point in an open ring."""

    for scenario, ring in sample_rings.items():
        if "open" in scenario:
            ring.insert_point(Point(x=-1, y=-1, ID=10), 1)

            assert len(ring._nodes) == len(sample_points[scenario]) + 1
            assert ring._nodes[1].value == Point(x=-1, y=-1, ID=10)


def test_ring_insert_point_closed(sample_rings, sample_points):
    """This tests inserting a new point in an closed ring."""

    for scenario, ring in sample_rings.items():
        if "closed" in scenario:
            ring.insert_point(Point(x=-1, y=-1, ID=10), 1)

            assert len(ring._nodes) == len(sample_points[scenario]) + 1
            assert ring._nodes[1].value == Point(x=-1, y=-1, ID=10)
            assert ring._nodes[0].right.value.ID == 10
            assert ring._nodes[1].left.value.ID == sample_points[scenario][0].ID
            assert ring._nodes[1].right.value.ID == sample_points[scenario][1].ID
            assert ring._nodes[2].left.value.ID == 10


@pytest.mark.parametrize(
    "scenario,orient1,orient2",
    [
        ("closed,CCW,convex", Orientation.CCW, Orientation.CW),
        ("closed,CW,convex", Orientation.CW, Orientation.CCW),
        ("closed,CCW,concave", Orientation.CCW, Orientation.CW),
        ("closed,CW,concave", Orientation.CW, Orientation.CCW),
    ]
)
def test_ring_reverse_orientation(
    sample_rings, sample_points, scenario, orient1, orient2
):
    """This tests the ability to reverse a ring's orientation."""

    ring: Ring = sample_rings[scenario]
    assert ring.orientation == orient1
    for n, node in enumerate(ring._nodes):
        n_before: int = n - 1
        n_after: int = (n + 1) % len(ring._nodes)

        assert node.left.value.ID == sample_points[scenario][n_before].ID
        assert node.right.value.ID == sample_points[scenario][n_after].ID

    ring.reverse_orientation()
    sample_points[scenario].reverse()
    assert ring.orientation == orient2
    for n, node in enumerate(ring._nodes):
        n_before: int = n - 1
        n_after: int = (n + 1) % len(ring._nodes)

        assert node.left.value.ID == sample_points[scenario][n_before].ID
        assert node.right.value.ID == sample_points[scenario][n_after].ID
