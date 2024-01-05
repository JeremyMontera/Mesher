import os
import pathlib

from .abc import IWriter
from mesher.geometry.abc import IRing

CWD: pathlib.Path = pathlib.Path(os.getcwd())

class Writer(IWriter):
    
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
