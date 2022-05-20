"""Engine Class"""

from NE.Entities.Base import Base
from NE.Entities.Bird import Bird
from NE.Entities.Pipe import Pipe

from enum import Enum
from typing import List, Tuple
from pygame import Surface
from pygame.sysfont import SysFont
from neat.config import Config
from neat.nn import FeedForwardNetwork
from neat import DefaultGenome

import neat
import pygame

FRAMES_PER_SECOND = 30
BIRD_POSITION_X = 220
BIRD_POSITION_Y = 350
BASE_POSITION_Y = 650
PIPE_POSITION_X = 650
FONT_SIZE = 42
TEXT_POSITION = 25
GENERATIONS = 150
FITNESS_INCREASE_PASS = 5
FITNESS_INCREASE_LIVE = 0.1
DECISION_BORDER = 0.5
FITNESS_DECREASE = 1


class AssetType(Enum):
    """

    Note:
    Asset type defines which category current asset belongs to.
    f.e BIRD_IMAGE defines assets with bird image as resource.

    """

    BIRD_IMAGE = (0,)
    BASE_IMAGE = (1,)
    BACKGROUND_IMAGE = (2,)
    PIPE_IMAGE = (3,)


class ScaleCriteria(Enum):
    """

    Note:
    While we want to display assets and resources properly we want to scale them in a correct way.
    What's more not all assets are going to be scaled in same way. Thus ScaleCriteria enumerate class
    defines criterias of scaling assets.

    If we would like to pick a custom size we need to provide it.

    """

    DOUBLE_SIZE = 1
    CUSTOM_SIZE = 2


class Engine:
    """

    Attributes:
    window_width: int
        - width of game window

    window_height: int
        - height of game window

    window: Surface
        - window object which defines game window

    assets: List[Tuple[AssetType, Surface]]
        - list of assets that are drawings of entities

    birds: List[Bird]
        - list of birds entity objects

    background: Surface
        - background object

    pipes: List[Pipe]
        - list of pipes entity objects

    base: Base
        - base entity object

    score: int
        - score attribute which defines current score reached by bird entity.

    window_font: SysFont
        - current font in game displayed on window

    neat_config: Config
        - configuration of basic neat

    networks: List[FeedForwardNetwork]
        - list of artificial neural networks that control each bird

    genomes: List[DefaultGenome]
        - list of genomes which evaluate fitness function properly

    Methods:
    load_asset(self, asset_type: AssetType, asset_path: str, scale: bool = True) -> None:
        - method which loads asset into game engine and scales it if needed

    init_neat(self, neat_config_filepath: str) -> None:
        - method which initializes neat configuration object

    run_ne(self, genomes, config: Config) -> None:
        - method which runs neuroevolution visualization on window

    draw_window(self) -> None:
        - method which draws each entity and defines business logic for game

    move_pipes(self) -> None:
        - method which is responsible for pipes moving on window

    emulate_birds(self) -> None:
        - method which emulates behavior of each bird controlled by neural network

    __init_window(self) -> None:
        - method which initializes window object

    __get_assets(self, asset_type: AssetType) -> List[Surface]:
        - method which returns all assets of given asset type
        f.e BIRD_IMAGE

    """

    window_width: int
    window_height: int
    window: Surface
    assets: List[Tuple[AssetType, Surface]]
    birds: List[Bird]
    background: Surface
    pipes: List[Pipe]
    base: Base
    score: int
    window_font: SysFont
    neat_config: Config
    networks: List[FeedForwardNetwork]
    genomes: List[DefaultGenome]

    def __init__(self, window_size: Tuple[int, int]) -> None:
        window_width, window_height = window_size
        self.window_width = window_width
        self.window_height = window_height
        self.assets = []
        self.score = 0

        self.birds = []
        self.networks = []
        self.genomes = []

        pygame.init()
        self.__init_window()

    def load_asset(
        self,
        asset_type: AssetType,
        asset_path: str,
        scale_criteria: ScaleCriteria = ScaleCriteria.DOUBLE_SIZE,
        custom_scale: Tuple[int, int] = (100, 100),
    ) -> None:
        asset_surface = pygame.image.load(asset_path)

        self.assets.append(
            (
                asset_type,
                pygame.transform.scale2x(asset_surface)
                if scale_criteria == ScaleCriteria.DOUBLE_SIZE
                else pygame.transform.scale(asset_surface, custom_scale),
            )
        )

    def init_neat(self, neat_config_filepath: str) -> None:
        """

        Note:
        This method is responsible for initializing basic neat. We are going to use a lot of
        default stuff provided by NEAT developers, also we want to include our configuration
        file provided.

        """

        self.neat_config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            neat_config_filepath,
        )

        population = neat.Population(self.neat_config)
        population.run(self.run_ne, GENERATIONS)

    def run_ne(self, genomes: List[DefaultGenome], config: Config) -> None:
        """

        Note:
        Running neuroevolution process starts with initializing networks, genomes, birds
        and picking appropriate assets with generating game window.

        """

        self.score = 0

        bird_images = self.__get_assets(AssetType.BIRD_IMAGE)
        pipe_image = self.__get_assets(AssetType.PIPE_IMAGE)[0]
        base_image = self.__get_assets(AssetType.BASE_IMAGE)[0]
        self.background = self.__get_assets(AssetType.BACKGROUND_IMAGE)[0]

        for _, genome in genomes:
            genome.fitness = 0
            current_network = neat.nn.FeedForwardNetwork.create(genome, config)
            self.networks.append(current_network)
            self.birds.append(Bird([BIRD_POSITION_X, BIRD_POSITION_Y], bird_images))

            self.genomes.append(genome)

        self.pipes = [Pipe(PIPE_POSITION_X, pipe_image)]
        self.base = Base(BASE_POSITION_Y, base_image)

        is_running = True
        clock = pygame.time.Clock()

        while is_running and len(self.birds) > 0:
            clock.tick(FRAMES_PER_SECOND)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                    pygame.quit()
                    break

            self.base.move()
            self.emulate_birds()
            self.move_pipes()
            self.draw_window()

    def draw_window(self) -> None:
        self.window.blit(self.background, (0, 0))

        for _, bird in enumerate(self.birds):
            bird.draw(self.window)

        for _, pipe in enumerate(self.pipes):
            pipe.draw(self.window)

        self.base.draw(self.window)

        current_score = self.window_font.render(
            f"Score {str(self.score)}", 1, (244, 244, 244)
        )

        self.window.blit(
            current_score,
            (
                self.window_width - current_score.get_width() - TEXT_POSITION,
                TEXT_POSITION,
            ),
        )
        pygame.display.update()

    def move_pipes(self) -> None:
        """

        Note:
        We want to keep track of each pipe that should be removed if it has passed screen. Let's
        assume that each passed pipe is placed into container which keeps track of removed pipes.

        Let's begin with empty container.

        What's more we would like to create new pipe each time current pipe has beed passed by bird
        entity. So we also need to keep track of the passing state between pipe and bird.

        There are several cases when we would like to remove some bird from training process because
        of their non-capable moves.

        If any bird has collision with any pipe we should remove this bird from training process, because
        it isn't the good entity so far. Also if bird hits border of our game window we should remove
        it from game.

        However if any bird passes pipes successfuly we should increase fitness function value in aim
        of maximizing results and finding optimal solution.

        """

        pipes_to_remove = []
        create_new_pipe = False

        for _, pipe in enumerate(self.pipes):

            for i, bird in enumerate(self.birds):
                if pipe.is_collision(bird):
                    self.genomes[i].fitness -= FITNESS_DECREASE
                    self.birds.pop(i)
                    self.networks.pop(i)
                    self.genomes.pop(i)

                if not pipe.is_passed and pipe.is_bird_passed(bird):
                    create_new_pipe = True

            if pipe.is_window_passed():
                pipes_to_remove.append(pipe)

            pipe.move()

        if create_new_pipe:
            pipe_image = self.__get_assets(AssetType.PIPE_IMAGE)[0]
            self.pipes.append(Pipe(PIPE_POSITION_X, pipe_image))
            self.score += 1

            for genome in self.genomes:
                genome.fitness += FITNESS_INCREASE_PASS

        for _, pipe_to_remove in enumerate(pipes_to_remove):
            self.pipes.remove(pipe_to_remove)

        for i, bird in enumerate(self.birds):
            if bird.hits_border():
                self.birds.pop(i)
                self.networks.pop(i)
                self.genomes.pop(i)

    def emulate_birds(self) -> None:
        """

        Note:
        This method emulates behavior of each bird controlled by neural network. Our neural networks
        consists of several inputs which defines what aspects of game are important for bird to
        come up with great solution and avoid pipes.

        Let's assume we want to pass three inputs into neural network which are:
        - actual bird position on y axis
        - difference between bird position on y axis and each mini pipe (two mini pipes)

        The FeedForwardNetwork emulates jumping strategy of each bird in birds collection. It's
        up to network if current bird jumps. If our neural network gets pretty well on this problem
        we are going to incrase fitness of each genome which is doing well, by this our function
        will gain higher value which is great in case to maximize fitness score. Also we should
        notice that our neural network predicts value between 0 and 1. Let's assume any value
        which is greater than 0.5 is positive one which determines jumping strategy while any value
        which is less than 0.5 is negative one with no jumping strategy.

        """

        current_pipe_index = 0

        if len(self.birds) > 0:
            if (
                len(self.pipes) > 1
                and self.birds[0].position[0]
                > self.pipes[0].position_x + self.pipes[0].mini_pipes[1].get_width()
            ):
                current_pipe_index = 1

        for i, bird in enumerate(self.birds):
            bird.move()
            self.genomes[i].fitness += FITNESS_INCREASE_LIVE

            output = self.networks[i].activate(
                (
                    bird.position[1],
                    abs(
                        bird.position[1] - self.pipes[current_pipe_index].position_y[0]
                    ),
                    abs(bird.position[1] - self.pipes[current_pipe_index].height),
                )
            )[0]

            if output > DECISION_BORDER:
                bird.jump()

    def __init_window(self) -> None:
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.window_font = pygame.font.SysFont("comicsans", FONT_SIZE)
        pygame.display.set_caption("Neuroevolution in Flappy Bird")

    def __get_assets(self, asset_type: AssetType) -> List[Surface]:
        return [asset[1] for asset in self.assets if asset[0] == asset_type]
