import os
import pathlib

from .abc import IReader
from mesher.geometry.point import Point
from mesher.geometry.ring import Ring

CWD: pathlib.Path = pathlib.Path(os.getcwd())

class Reader(IReader):

    """
    This class implements a basic reader class. It will read geometric data from a
    geometry file (right now, a text file). A geometry file currently consists of a
    ring name and the points in the order they should be loaded in. This class should
    not be directly created by the user.
    """

    @staticmethod
    def read(filename: str | pathlib.Path) -> list[Ring]:
        """
        Read point data from file and load it into figures.

        TODO: update this when polygons/cells are implemented.
        TODO: handle filepaths more gracefully...

        Args:
            filename:
                File to read geometric data from (assumed not to include the full path,
                we will let this do the work for now).

        Returns:
            data:
                Geometric data from file.
        """

        if isinstance(filename, str):
            filename: pathlib.Path = pathlib.Path(filename)

        filepath: pathlib.Path = CWD / filename
        if not os.path.exists(filepath):
            raise OSError(f"{filepath} doesn't exist!")
        
        with open(filepath, "r") as f:
            data: dict[str, Ring] = {}
            current_name: str | None = None
            for line in f.readlines():
                content: list[str] = line.rstrip().split(",")
                if len(content) == 1:
                    data[content[0]] = Ring()
                    current_name = content[0]

                else:
                    x: float = float(content[0])
                    y: float = float(content[1])
                    ID: int = int(content[2])
                    data[current_name].add_point(Point(x=x, y=y, ID=ID))

        return data
