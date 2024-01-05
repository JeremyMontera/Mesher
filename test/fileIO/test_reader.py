import os
import pathlib
import pytest
from unittest import mock

from mesher.fileIO.reader import Reader
from mesher.geometry.point import Point
from mesher.geometry.ring import Ring

class TestReader:

    filename: pathlib.Path = pathlib.Path("test/fileIO/test_ring_data.txt")

    @mock.patch("os.path.exists")
    def test_reader_read_error_file_not_found(self, mock_exists):
        mock_exists.return_value = False
        with pytest.raises(OSError) as exc:
            Reader.read(self.filename)

        filepath: pathlib.Path = pathlib.Path(os.getcwd()) / self.filename
        assert exc.value.args[0] == f"{filepath} doesn't exist!"

    def test_reader_read(self):
        data: dict[str, Ring] = Reader.read(self.filename)
        assert len(data) == 2
        assert "foo" in data.keys()
        assert len(data["foo"]) == 3
        assert Point(x=0, y=0, ID=0) in data["foo"]
        assert Point(x=1, y=0, ID=1) in data["foo"]
        assert Point(x=1, y=1, ID=2) in data["foo"]
        assert "bar" in data.keys()
        assert len(data["bar"]) == 4
        assert Point(x=0, y=0, ID=3) in data["bar"]
        assert Point(x=1, y=1, ID=4) in data["bar"]
        assert Point(x=0, y=2, ID=5) in data["bar"]
        assert Point(x=-1, y=1, ID=6) in data["bar"]