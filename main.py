from NE.Engine.Engine import AssetType, Engine, ScaleCriteria
import os

local_directory = os.path.dirname(__file__)
neat_configuration_file = os.path.join(local_directory, "neuroevolution-config.txt")

game_engine = Engine((600, 800))
game_engine.load_asset(AssetType.BIRD_IMAGE, os.path.join("assets", "bird1.png"))
game_engine.load_asset(AssetType.BIRD_IMAGE, os.path.join("assets", "bird2.png"))
game_engine.load_asset(AssetType.BIRD_IMAGE, os.path.join("assets", "bird3.png"))
game_engine.load_asset(AssetType.BASE_IMAGE, os.path.join("assets", "base.png"))
game_engine.load_asset(
    AssetType.BACKGROUND_IMAGE,
    os.path.join("assets", "bg.png"),
    ScaleCriteria.CUSTOM_SIZE,
    (600, 900),
)
game_engine.load_asset(AssetType.PIPE_IMAGE, os.path.join("assets", "pipe.png"))
game_engine.init_neat(neat_configuration_file)
