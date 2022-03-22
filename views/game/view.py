from core.node import Node
from core.actor import Actor
from core.space import Space
from core.sprite import Sprite
from core.body import Body
from components.tilemap import TileMap
from components.camera import Camera

from random import choice

from pymunk.vec2d import Vec2d as Vector


class GameView(Node):
    def fit(self):
        super().fit()


class Player(Actor):
    animations = {
        'idle': {
            'left': [183],
            'right': [168]
        },
        'moving': {
            'left': [183, 182, 181, 180, 181, 182],
            'right': [168, 169, 170, 171, 170, 169]
        }
    }

    def fit(self):
        super().fit()
        self.get_root().events.connect('on_key_pressed', 'move_up', f'{self.get_path()}/move_up')
        self.get_root().events.connect('on_key_pressed', 'move_left', f'{self.get_path()}/move_left')
        self.get_root().events.connect('on_key_pressed', 'move_right', f'{self.get_path()}/move_right')
        self.get_root().events.connect('on_key_pressed', 'move_down', f'{self.get_path()}/move_down')
        self.initattr('direction', 'W')
        self.radial = 'right'
        self.frame_types = {
            'idle': 'fixed',
            'moving': 'velocity',
        }
        self.set_index(168)

    def build(self):
        self(
            self.name,
        )
        super().build()

    def on_collision(self, arbiter, space, data):
        return False

    def handle_animation(self):
        if self.radial_trigger():
            if self.radial == 'left':
                self.mirror()
            else:
                self.reset()

        animation = self.animations[self.get_state()][self.radial]
        frame_index = int(
            (getattr(self, f'{self.frame_types[self.state]}_frames') / self.framerate) % len(animation)
        )
        self.set_index(animation[frame_index])

    def get_state(self) -> str:
        if self.velocity.length > 0.1:
            return 'moving'
        else:
            return 'idle'

    def move_up(self):
        force = Vector(0, -self.acceleration * self.get_root().delta)
        self.impulse(force)
        self.set_heading()

    def move_left(self):
        force = Vector(-self.acceleration * self.get_root().delta, 0)
        self.impulse(force)
        self.radial = 'left'
        self.set_heading()

    def move_right(self):
        force = Vector(self.acceleration * self.get_root().delta, 0)
        self.impulse(force)
        self.radial = 'right'
        self.set_heading()

    def move_down(self):
        force = Vector(0, self.acceleration * self.get_root().delta)
        self.impulse(force)
        self.set_heading()

    async def loop(self):
        self.handle_frames()
        self.handle_animation()
        await super().loop()


class FloorTile(Sprite):
    def build(self):
        self(
            self.name,
            anchor='topleft',
            size=(16, 16),
            cols=32,
            rows=32,
            scale=1,
            resource='../../../../../../resources/spritesheet',
        )

        super().build()

    def fit(self):
        super().fit()
        self.set_index(choice([129, 130, 131, 161, 162, 163]))


class VerticalWallEdgeTile(Sprite):
    def build(self):
        self(
            self.name,
            body_type='static',
            anchor='topleft',
            size=(16, 16),
            cols=32,
            rows=32,
            resource='../../../../../../resources/spritesheet',
        )

    def fit(self):
        super().fit()
        self.set_index(2)


class VerticalWallTile(Body, Sprite):
    def build(self):
        self(
            self.name,
            body_type='static',
            anchor='topleft',
            size=(16, 16),
            cols=32,
            rows=32,
            resource='../../../../../../resources/spritesheet',
            vertices=[[-8, -8], [-8, 8], [8, 8], [8, -8]],
        )

    def fit(self):
        super().fit()
        self.set_index(34)


class HorizontalWallTile(Body, Sprite):
    def build(self):
        self(
            self.name,
            body_type='static',
            anchor='topleft',
            size=(16, 16),
            cols=32,
            rows=32,
            resource='../../../../../../resources/spritesheet',
            vertices=[[-8, -8], [-8, 8], [8, 8], [8, -8]],
        )

    def fit(self):
        super().fit()
        self.set_index(289)


TILESET = {
    1: FloorTile,
    3: VerticalWallEdgeTile,
    4: HorizontalWallTile,
    2: VerticalWallTile,
    0: Node,
}


game = GameView(
    'game',
    Camera(
        'camera',
        Space(
            'collision_layer',
            # TileMap(
            #     'tilemap_layer_1',
            #     tileset=TILESET,
            #     matrix=[
            #         [0 for _ in range(20)],
            #         [2 for _ in range(20)],
            #         [1 for _ in range(20)],
            #         [1 for _ in range(20)],
            #         [1 for _ in range(20)],
            #         [1 for _ in range(20)],
            #         [1 for _ in range(20)],
            #         [1 for _ in range(20)],
            #         [1 for _ in range(20)],
            #         [1 for _ in range(20)],
            #     ],
            #     position=(0, 0),
            # ),
            Player(
                'player',
                resource='../../../../../resources/spritesheet',
                position=(64, 64),
                density=1,
                size=(16, 32),
                cols=32,
                rows=16,
                vertices=[[-5, 3], [5, 3], [5, 13], [-5, 13]],
            ),
            TileMap(
                'tilemap_layer_2',
                tileset=TILESET,
                matrix=[
                    [3 for _ in range(20)],
                    [0 for _ in range(20)],
                    [0 for _ in range(20)],
                    [0 for _ in range(20)],
                    [0 for _ in range(20)],
                    [0 for _ in range(20)],
                    [0 for _ in range(20)],
                    [0 for _ in range(20)],
                    [0 for _ in range(20)],
                    [3 for _ in range(20)],
                    [2 for _ in range(20)]
                ],
                position=(0, 0),
            ),

            gravity=[0, 0],
        ),
        target='collision_layer/player'
    ),
)
