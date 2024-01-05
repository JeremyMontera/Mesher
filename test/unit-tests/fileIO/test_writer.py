import os
import pathlib
from unittest import mock

import pytest

from mesher.fileIO.writer import Writer
from mesher.geometry.point import Point
from mesher.geometry.ring import Ring


class TestWriter:
    filename: pathlib.Path = pathlib.Path("test.txt")

    def setup_point_info(self):
        """Setup some simple geometry data."""

        ring0: Ring = Ring()
        ring0.add_point(Point(x=0, y=0, ID=0))
        ring0.add_point(Point(x=1, y=0, ID=1))
        ring0.add_point(Point(x=1, y=1, ID=2))

        ring1: Ring = Ring()
        ring1.add_point(Point(x=0, y=0, ID=3))
        ring1.add_point(Point(x=1, y=1, ID=4))
        ring1.add_point(Point(x=0, y=2, ID=5))
        ring1.add_point(Point(x=-1, y=1, ID=6))

        self.data: dict[str, Ring] = {
            "foo": ring0,
            "bar": ring1,
        }

    @mock.patch("os.path.exists")
    def test_writer_error_file_exists(self, mock_exists):
        """Test that the writer raises an error if the file already exists."""

        mock_exists.return_value = True
        with pytest.raises(OSError) as exc:
            Writer.write(self.filename, {})

        filepath: pathlib.Path = pathlib.Path(os.getcwd()) / self.filename
        assert exc.value.args[0] == f"{filepath} already exists!"

    def test_writer_write(self):
        """Test that the writer writes the data to the geometry file."""

        assert not os.path.exists(self.filename)
        self.setup_point_info()
        Writer.write(self.filename, self.data)
        assert os.path.exists(self.filename)
        os.remove(self.filename)
