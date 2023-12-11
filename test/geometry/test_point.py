import pytest

from mesher.geometry.point import Point, cross_product


@pytest.fixture
def sample_data() -> dict[str, list[int | float]]:
    """Data for generating sample points."""

    return {
        "ID": [121, -45],
        "x": [3.2, -0.2],
        "y": [-4.6, 0.04],
    }


@pytest.fixture
def sample_points(sample_data: dict[str, list[int | float]]) -> list[Point]:
    """Generate two sample points: user-defined and auto-defined."""

    return [
        Point(x=sample_data["x"][0], y=sample_data["y"][0], ID=sample_data["ID"][0]),
        Point(x=sample_data["x"][1], y=sample_data["y"][1], ID=sample_data["ID"][1]),
    ]


def test_point_init(sample_data, sample_points):
    """This tests point construction and point attributes."""

    for p, point in enumerate(sample_points):
        for key, val in sample_data.items():
            assert hasattr(point, f"_{key}")
            assert getattr(point, f"_{key}") == val[p]
            assert getattr(point, f"{key}") == val[p]


@pytest.mark.parametrize(
    "op",
    [
        lambda x, y: x + y,
        lambda x, y: x - y,
    ],
)
def test_point_ops(op, sample_data, sample_points):
    """This tests point addition and subtraction."""

    for p in range(len(sample_points)):
        p1: int = p
        p2: int = (p + 1) % len(sample_points)

        assert op(sample_points[p1], sample_points[p2]) == Point(
            x=op(sample_data["x"][p1], sample_data["x"][p2]),
            y=op(sample_data["y"][p1], sample_data["y"][p2]),
            ID=sample_data["ID"][p1] + sample_data["ID"][p2],
        )


def test_point_equals(sample_points):
    """This tests point equality (within tolerance)."""

    for point in sample_points:
        good: Point = Point(x=point._x - 1e-12, y=point._y + 5e-14, ID=1)
        bad: Point = Point(x=point._x + 3e-4, y=point._y - 6e-8, ID=-1)

        assert point == good
        assert point != bad


def test_point_string(sample_data, sample_points):
    """This tests that the point is printed correctly."""

    for p, point in enumerate(sample_points):
        x: float = sample_data["x"][p]
        y: float = sample_data["y"][p]
        ID: int = sample_data["ID"][p]
        assert str(point) == f"Point(x={x}, y={y}, ID={ID})"


def test_cross_product(sample_data, sample_points):
    """This tests the cross product between points."""

    for p in range(len(sample_points)):
        p1: int = p
        p2: int = (p + 1) % len(sample_points)
        ret: float = (
            sample_data["x"][p1] * sample_data["y"][p2]
            - sample_data["x"][p2] * sample_data["y"][p1]  # noqa: W503
        )

        assert cross_product(sample_points[p1], sample_points[p2]) == ret
