"""Bird Class"""

from NE.Entities.Entity import Entity

from typing import List
from pygame import Surface
from pygame.mask import Mask
import pygame

BIRD_JUMP_VELOCITY = -10
BIRD_TERMINAL_VELOCITY = 16
BIRD_MAX_ROTATION = 25
BIRD_OFFSET = 680


class Bird(Entity):
    """

    Attributes:
    position: List[int]
        - position of bird entity on game window
        Position list contains two isolated attributes which defines coordinates of
        entity position on window

    rotation: int
        - current rotation of bird entity during move

    velocity: int
        - current velocity of bird entity during move

    jump_position: int
        - current position of bird while jumping has started

    animation_frame: int
        - animation frame which describes the image which is ready to draw

    tick_frame: int
        - tick frame which describes the gravity force which affects bird entity

    images: List[Surface]
        - list of images that are responsible for animating entity

    image: Surface
        - current image of bird that is displayed on game window

    Methods:
    move(self) -> None:
        - method which is inherited from base class

    draw(self, window: Surface) -> None:
        - method which is inherited from base class

    jump(self) -> None:
        - method which is responsible for bird entity jumps

    hits_border(self) -> bool:
        - method which returns if current bird entity hits any border

    get_mask(self) -> Mask:
        - method which returns mask matrix for bird entity surface

    """

    position: List[int]
    rotation: int
    velocity: int
    jump_position: int
    animation_frame: int
    tick_frame: int
    images: List[Surface]
    image: Surface

    def __init__(self, position: List[int], images: List[Surface]) -> None:
        self.position = position
        self.rotation = self.velocity = 0
        self.jump_position = self.position[1]
        self.animation_frame = self.tick_frame = 0
        self.images = images
        self.image = self.images[self.animation_frame]

    def move(self) -> None:
        """

        Note:
        Each frame we want to move our bird entity in one of two directions UP or DOWN, the distance
        variable describes which direction and how quick we want to move.

        For any negative distance we want to move up, while if any other case we want to move down.
        The distance formula is given as below:

        distance = velocity * tick + 1.5 * tick^2

        Let's simplify it a little bit
        If velocity is equal to 0, then our distance is positive (tick + 1.5 * tick^2), then we are
        moving towards ground. However if our velocity is negative, our formula changes a little bit
        and we are minimizing the gravity and increasing the jumping force.

        """

        self.tick_frame += 1

        distance = self.velocity * self.tick_frame + 1.5 * self.tick_frame**2
        if distance >= BIRD_TERMINAL_VELOCITY:
            distance = BIRD_TERMINAL_VELOCITY

        self.position[1] += distance

        if distance < 0 or self.position[1] < self.jump_position:
            self.rotation = BIRD_MAX_ROTATION
        else:
            self.rotation = -BIRD_MAX_ROTATION

    def draw(self, window: Surface) -> None:
        """

        Note:
        Each frame we want to increase animation frame counter in aim of changing animation image.
        What's more we want to rotate this image about angle which is defined by internal
        rotation. However anchor point of rotation is defined as top left corner of surface.
        If we want to make it look more naturally we should change anchor point to center of the
        surface.

        """

        self.animation_frame += 1
        self.image = self.images[self.animation_frame % len(self.images)]

        rotated_image = pygame.transform.rotate(self.image, self.rotation)
        anchor_rectangle = rotated_image.get_rect(
            center=self.image.get_rect(
                topleft=(self.position[0], self.position[1])
            ).center
        )
        window.blit(rotated_image, anchor_rectangle.topleft)

    def jump(self) -> None:
        """

        Note:
        Jump position contains value of position on y axis while the jumping has started. We want
        to keep track of previous position of jump in aim of animating the bird properly.

        """

        self.velocity = BIRD_JUMP_VELOCITY
        self.jump_position = self.position[1]
        self.tick_frame = 0

    def hits_border(self) -> bool:
        return (
            self.position[1] + self.image.get_height() >= BIRD_OFFSET
            or self.position[1] < 0
        )

    def get_mask(self) -> Mask:
        """

        Note:
        Mask is represented as binary matrix.

        """

        return pygame.mask.from_surface(self.image)
