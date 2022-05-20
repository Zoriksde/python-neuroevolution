"""Base Class"""

from typing import List
from pygame import Surface
from NE.Entities.Entity import Entity

BASE_VELOCITY = 5


class Base(Entity):
    """

    Attributes:
    position_x: List[int]
        - position on x axis of base entity on game window

    position_y: int
        - position on y axis of base entity on game window

    image: Surface
        - current image of base that is displayed on game window

    Methods:
    move(self) -> None:
        - method which is inherited from base class

    draw(self, window: Surface) -> None:
        - method which is inherited from base class

    Note:
    Base drawing consists of two images of our base. Animation process ensures us that the animation
    is correctly displayed. We are keeping track of two positions on x axis of our base images.
    What's more we need to identify which image to display first.

    Let's visualize a problem:

    [xxxxxxxxxxx] - base drawing
    [xxxxxxxxxx-] - base drawing after one frame
    [xxxx-------] - base drawing after some frames

    We would like to avoid this situation, so let's assume there exists second base image

    [xxxxxcccccc] - base drawing with two images after some frames
    [cccccxxxxxx] - base drawing with two images after some more frames

    Where:
    x - represents a base image
    c - represents second base image

    """

    position_x: List[int]
    position_y: int
    image: Surface

    def __init__(self, position_y: int, image: Surface) -> None:
        self.position_x = [0, image.get_width()]
        self.position_y = position_y
        self.image = image

    def move(self) -> None:
        """

        Note:
        We need to decrease position on x axis of each image after each frame. Thus
        our list of positions is changed. Then for each position we are swapping images in
        some way. This behaviour represents an animation process of moving base.

        """

        self.position_x = [current_x - BASE_VELOCITY for current_x in self.position_x]

        for i, base_position_x in enumerate(self.position_x):
            if base_position_x + self.image.get_width() < 0:
                self.position_x[i] = (
                    self.position_x[(i + 1) % 2] + self.image.get_width()
                )

    def draw(self, window: Surface) -> None:
        for _, base_position_x in enumerate(self.position_x):
            window.blit(self.image, (base_position_x, self.position_y))
