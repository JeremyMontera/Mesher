import abc
import pathlib

from mesher.geometry.abc import IRing


class IReader(metaclass=abc.ABCMeta):

    """This is an interface for the [`Reader`][mesher.fileIO.reader.Reader] class."""

    @staticmethod
    @abc.abstractmethod
    def read(filename: str | pathlib.Path) -> list[IRing]:
        """
        Read point data from file and load it into figures.

        TODO: update this when polygons/cells are implemented.
        """

        ...


class IWriter(metaclass=abc.ABCMeta):

    """This is an interface for the [`Writer`][mesher.fileIO.writer.Writer] class."""

    @staticmethod
    @abc.abstractmethod
    def write(filename: str | pathlib.Path, data: dict[str, IRing]) -> None:
        """
        Write point data from figures to file.

        TODO: update this when polygons/cells are implemented.
        """

        ...
