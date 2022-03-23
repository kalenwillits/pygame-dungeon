from core.node import Node
from core.space import Space
from components.map import Map
from components.camera import Camera
from views.game.player import Player
from views.game.tiles.dungeon_tiles import TILESET
from views.game.map import MAP

# TODO Radials constant dict


class Game(Node):
    def build(self):
        self(
            self.name,
            Camera(
                'camera',
                Space(
                    'collision_layer',
                    Map(
                        'map',
                        Player(
                            'player',
                            resource='/resources/spritesheet',
                            position=(64, 64),
                            size=(16, 32),
                            vertices=[(-5, 8), (5, 8), (5, 16), (-5, 16)],
                            cols=32,
                            rows=16,
                        ),
                        tileset=TILESET,
                        tilesize=(32, 32),
                        matrix=MAP,
                        position=(0, 0),
                    ),
                    gravity=[0, 0],
                ),
                target='collision_layer/map/player'
            ),
        )
        super().build()
