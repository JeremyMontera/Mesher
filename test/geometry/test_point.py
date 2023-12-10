import pytest

from mesher.geometry.point import Point


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
