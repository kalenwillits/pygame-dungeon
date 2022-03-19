from core.node import Node
from core.actor import Actor
from core.space import Space
from core.sprite import Sprite
from core.body import Body
from components.tilemap import TileMap
from components.camera import Camera
from core.resource import Resource


class GameView(Node):
    def fit(self):
        super().fit()

    async def loop(self):
        await super().loop()


class Player(Actor):
    sync_rotation = False
    animation_state: str = None

    def fit(self):
        super().fit()
        self.get_root().events.connect('on_key_pressed', 'move_up', f'{self.get_path()}/move_up')
        self.get_root().events.connect('on_key_pressed', 'move_left', f'{self.get_path()}/move_left')
        self.get_root().events.connect('on_key_pressed', 'move_right', f'{self.get_path()}/move_right')
        self.get_root().events.connect('on_key_pressed', 'move_down', f'{self.get_path()}/move_down')

    def build(self):
        self(
            self.name,
        )
        super().build()

    def on_collision(self, arbiter, space, data):
        return True

    def handle_animation(self):
        ...

    def move_up(self):
        self.impulse((0, -self.acceleration * self.get_root().delta))
        self.set_radial((self.velocity.x, -1))

    def move_left(self):
        self.impulse((-self.acceleration * self.get_root().delta, 0))
        self.set_radial((-1, self.velocity.y))

    def move_right(self):
        self.impulse((self.acceleration * self.get_root().delta, 0))
        self.set_radial((1, self.velocity.y))

    def move_down(self):
        self.impulse((0, self.acceleration * self.get_root().delta))
        self.set_radial((self.velocity.x, 1))

    async def loop(self):
        await super().loop()


game = GameView(
    'game',
    Camera(
        'camera',
        Space(
            'collision_layer',
            TileMap(
                'tilemap',
                matrix=[],
            ),
            Player(
                'player',
                resource='../../../../../spritesheet',
                position=(500, 500),
                density=1,
                size=(16, 16),
                scale=6,
            ),
            gravity=[0, 0],
        ),
        target='collision_layer/player'
    ),
)
