"""Pipe Class"""

from NE.Entities.Bird import Bird
from NE.Entities.Entity import Entity

from random import randrange
from typing import List
from pygame import Surface
import pygame

PIPE_GAP = 300
PIPE_VELOCITY = 5
PIPE_MIN_HEIGHT = 50
PIPE_MAX_HEIGHT = 450


class Pipe(Entity):
    """

    Attributes:
    position_x: int
        - position on x axis of pipe entity on game window

    is_passed: bool
        - attribute which determines whether pipe is already passed

    mini_pipes: List[Surface]
        - list of mini pipes which define bigger pipe

    position_y: List[float]
        - list of position on y axis of each mini pipe

    height: float
        - height of current pipe

    Methods:
    move(self) -> None:
        - method which is inherited from base class

    draw(self, window: Surface) -> None:
        - method which is inherited from base class

    is_collision(self, bird: Bird) -> bool:
        - method which determines whether collision between bird and pipe occurs.

    is_window_passed(self) -> bool:
        - method which returns whether current pipe entity passed a game window.

    is_bird_passed(self, bird: Bird) -> bool:
        - method which returns whether current pipe entity passed a bird entity object.

    __init_pipe(self) -> None:
        - method which initializes pipe object

    Note:
    Pipe consists of two mini pipes, each mini pipe is place on same position on x axis. What's more
    these pipes are strongly correlated with each other. One of them is top pipe while the other is
    bottom one. Between mini pipes there is a gap which ensures that it's possible to come through it.

    Thus images container contains two surfaces each is responsible for one and only one mini pipe.
    The first one is responsible for bottom one whereas the second is reserved for top.

    """

    position_x: int
    is_passed: bool
    mini_pipes: List[Surface]
    position_y: List[float]
    height: float

    def __init__(self, position_x: int, image: Surface) -> None:
        self.position_x = position_x
        self.is_passed = False
        self.mini_pipes = [image, pygame.transform.flip(image, False, True)]
        self.position_y = [0, 0]
        self.height = 0

        self.__init_pipe()

    def move(self) -> None:
        """

        Note:
        Pipe moving is defined only by decresing position on x axis. Thus our mini pipes position
        on y axis remains.

        """

        self.position_x -= PIPE_VELOCITY

    def draw(self, window: Surface) -> None:
        for i, pipe_position_y in enumerate(self.position_y):
            window.blit(self.mini_pipes[i], (self.position_x, pipe_position_y))

    def is_collision(self, bird: Bird) -> bool:
        """

        Note:
        There are a lot of collision algorithms f.e AABB, Pixel Perfection Collision etc.
        We would like to have a perfect collision instead of intersection between two hitboxes.
        Thus we will convert our surfaces of each entity into masks, which allows us to determine
        if perfect collision occurs.

        Let's visualize a problem:

        bird_mask =
        [
            [0, 1, 1]
            [1, 1, 1]
            [1, 1, 0]
        ]

        Each mask is defined as binary matrix which contains 1 only if the pixel occurs, 0 otherwise.
        Then our algorithm compares two matrices composed as a masks and figures if any pixel is
        occuring in both matrices. If so, then we should handle collision which occurs, otherwise there
        is no collision detected.

        """

        bird_mask = bird.get_mask()

        mini_pipes_masks = [
            pygame.mask.from_surface(self.mini_pipes[0]),
            pygame.mask.from_surface(self.mini_pipes[1]),
        ]

        offsets = [
            (
                self.position_x - bird.position[0],
                self.position_y[0] - round(bird.position[1]),
            ),
            (
                self.position_x - bird.position[0],
                self.position_y[1] - round(bird.position[1]),
            ),
        ]

        bottom_overlap = bird_mask.overlap(mini_pipes_masks[0], offsets[0])
        top_overlap = bird_mask.overlap(mini_pipes_masks[1], offsets[1])

        return bottom_overlap or top_overlap

    def is_window_passed(self) -> bool:
        """

        Note:
        If current pipe entity passed a window, it ensures as that its position on x axis increased
        by a width of current pipe is negative.

        position_x + pipe_width < 0 <=> pipe has passed screen.

        """

        return self.position_x + self.mini_pipes[0].get_width() < 0

    def is_bird_passed(self, bird: Bird) -> bool:
        if self.position_x < bird.position[0]:
            self.is_passed = True

        return self.is_passed

    def __init_pipe(self) -> None:
        self.height = randrange(PIPE_MIN_HEIGHT, PIPE_MAX_HEIGHT)

        self.position_y = [
            self.height + PIPE_GAP,
            self.height - self.mini_pipes[1].get_height(),
        ]
