import os
import pathlib

from .abc import IWriter
from mesher.geometry.abc import IRing

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

        if os.path.exists(filename):
            raise OSError(f"{filename} already exists!")

        with open(filename, "w") as f:
            for name, ring in data.items():
                f.write(f"{name}\n")
                for point in ring:
                    f.write(f"{point.x},{point.y},{point.ID}\n")
