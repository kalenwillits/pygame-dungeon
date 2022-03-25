from core.node import Node
from core.space import Space
from components.map import Map
from components.camera import Camera
from views.game.player import Player
from views.game.map import MAP, TILESET

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
                            acceleration=50,
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
