"""Entity Class"""

from abc import ABC, abstractmethod
from pygame import Surface


class Entity(ABC):
    """

    Methods:
    move(self) -> None:
        - method which is responsible for entity move

    draw(self, window: Surface) -> None:
        - method which is responsible for drawing entity on window.

    """

    @abstractmethod
    def move(self) -> None:
        pass

    @abstractmethod
    def draw(self, window: Surface) -> None:
        pass
