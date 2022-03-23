from core.node import Node
from core.space import Space
from components.tilemap import TileMap
from components.camera import Camera
from views.game.player import Player
from views.game.tiles.dungeon_tiles import TILESET


# TODO Radials constant dict


class Game(Node):
    def build(self):
        self(
            self.name,
            Camera(
                'camera',
                Space(
                    'collision_layer',
                    TileMap(
                        'tilemap',
                        tileset=TILESET,
                        tilesize=(32, 32),
                        matrix=[
                            [3 for _ in range(20)],
                            [2 for _ in range(20)],
                            [1 for _ in range(20)],
                            [1 for _ in range(20)],
                            [1 for _ in range(20)],
                            [1 for _ in range(20)],
                            [1 for _ in range(20)],
                            [1 for _ in range(20)],
                            [1 for _ in range(20)],
                            [3 for _ in range(20)],
                            [2 for _ in range(20)],
                        ],
                        position=(0, 0),
                    ),
                    Player(
                        'player',
                        resource='../../../../../resources/spritesheet',
                        position=(64, 64),
                        sort=10,
                        density=1,
                        size=(16, 32),
                        cols=32,
                        rows=16,
                        vertices=[[-5, 3], [5, 3], [5, 13], [-5, 13]],
                    ),
                    gravity=[0, 0],
                ),
                target='collision_layer/player'
            ),
        )
        super().build()
