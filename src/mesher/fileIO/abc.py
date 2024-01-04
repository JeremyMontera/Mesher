import abc
import pathlib

from mesher.geometry.abc import IRing

class IReader(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def read(filename: str | pathlib.Path) -> list[IRing]:
        """
        Read point data from file and load it into figures.

        TODO: update this when polygons/cells are implemented.
        """

        ...
        

class IWriter(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def write(filename: str | pathlib.Path, data: dict[str, IRing]) -> None:
        """
        Write point data from figures to file.

        TODO: update this when polygons/cells are implemented.
        """
        
        ...