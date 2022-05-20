# Neuroevolution

Neuroevolution project that helps others to understand basic ideas behind neural networks and genetics algorithms.
The only requirement of understanding concepts of this project is basic knowledge of neural networks and genetics algorithms.
Project also consists of Flappy Bird game written from scratch which allows us to simulate behaviour of neuroevolution process.
Project is written in Python with NEAT.

The structure of game is divided into several different entities:

- Bird - which is responsible for visualizing moves of bird.
- Pipe - which is responsible for animating moving pipes in aim to handle business logic of game
- Base - which performs only animations of base entity.

Project is written using OOP Principles, which makes it easy to maintain, extend, fix and change.
Each entity object is implemented as single class which inherits from abstract one.

Ex. of base entity:

```python
class Base(Entity):
    position_x: List[int]
    position_y: int
    image: Surface

    def __init__(self, position_y: int, image: Surface) -> None:
        self.position_x = [0, image.get_width()]
        self.position_y = position_y
        self.image = image

    def move(self) -> None:
        self.position_x = [current_x - BASE_VELOCITY for current_x in self.position_x]

        for i, base_position_x in enumerate(self.position_x):
            if base_position_x + self.image.get_width() < 0:
                self.position_x[i] = (
                    self.position_x[(i + 1) % 2] + self.image.get_width()
                )

    def draw(self, window: Surface) -> None:
        for _, base_position_x in enumerate(self.position_x):
            window.blit(self.image, (base_position_x, self.position_y))
```

There is also Game Engine class which is responsible for initializing neuroevolution process and handling game state.

Ex. of running neuroevolution

```python
def init_neat(self, neat_config_filepath: str) -> None:
        self.neat_config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            neat_config_filepath,
        )

        population = neat.Population(self.neat_config)
        population.run(self.run_ne, GENERATIONS)
```

Notice that ```neuroevolution-config.txt``` file is configuration file which is responsible for proper initialization of
NEAT. If you want to play around with it, change some options and try make your own neuroevolution.

Assets directory contains images of each entity we want to display on window game.
Also notice the bird entity is the only one with image based animation so there is several images of one bird entity.

I do recommend this [article](https://arxiv.org/pdf/2006.05415.pdf) to read about neuroevolution concepts.

There is implemented game in ```main.py```.

Project is written with main aim to help anyone who is interested in these topics. Enjoy playing around!
