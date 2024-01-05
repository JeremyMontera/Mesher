import os
import pathlib

from mesher.geometry.abc import IRing

from .abc import IWriter

CWD: pathlib.Path = pathlib.Path(os.getcwd())


class Writer(IWriter):

    """
    This class implements a basic writer class. It will write geometric data to a
    geometry file (right now, a text file). A geometry file currently consists of a
    ring name and the points in the order they appear in the ring this class is writing
    to file. This class should not be directly created by the user.
    """

    @staticmethod
    def write(filename: str | pathlib.Path, data: dict[str, IRing]) -> None:
        """
        Write point data from figures to file.

        TODO: update this when polygons/cells are implemented.

        Args:
            filename:
                File to write geometric data to.
            data:
                Dictionary of ring names and rings.
        """

        if isinstance(filename, str):
            filename: pathlib.Path = pathlib.Path(filename)

        filepath: pathlib.Path = CWD / filename
        if os.path.exists(filepath):
            raise OSError(f"{filepath} already exists!")

        with open(filepath, "w") as f:
            for name, ring in data.items():
                f.write(f"{name}\n")
                for point in ring:
                    f.write(f"{point.x},{point.y},{point.ID}\n")
