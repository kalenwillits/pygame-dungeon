from math import pi
from collections import defaultdict
from pymunk.vec2d import Vec2d as Vector

from core.node import Node
from core.body import Body
from core.sprite import Sprite
from components.trigger import Trigger


class Stats(Node):
    health: int = None

    armor: int = None
    resist: int = None
    dodge: int = None

    def get_max_health(self) -> int:
        return self.strength // 2

    def get_speed(self) -> int:
        return self.agility / 2

    @property
    def strength(self):
        return self['/cache']['character']['strength']

    @property
    def agility(self):
        return self['/cache']['character']['agility']

    @property
    def intellect(self):
        return self['/cache']['character']['intellect']

    @property
    def experience(self):
        return self['/cache']['character']['experience']

    @property
    def classe_level(self):
        multiplier = 100  # Used to multiply how much xp is needed for each level
        exponent = 1.5  # exponent to increase how much each level takes to level up
        return int((self['/cache']['character']['experience'] / multiplier)**(1 / exponent))

    def fit(self):
        super().fit()


class Player(Body, Sprite):
    vertices = [[-10, 30], [-10, 6], [2, 0], [12, 6], [12, 30]]
    direction: str = 'E'
    state: str = None
    previous_state: str = None
    radial: str = None
    heading: float = None  # Intended direction in radians
    motion: Vector = None  # Movement that is about to be applied.
    frames: int = None
    framerate: int = None
    radial_precision: int = None
    animations: dict[
        str,  # animation name
        dict[
            str,  # radial
            list[
                int, ...  # sprite sheet indexes
            ]
        ]
    ] = None
    frame_types: defaultdict[str, str] = None

    def build(self):
        self(
            self.name,
            Stats(
                'stats'
            ),
            Trigger(
                'radial_trigger',
                value='../radial'
            )

        )
        super().build()

    def fit(self):
        self.initattr('motion', Vector(0, 0))
        self.initattr('state', self.get_root().settings.animation.state)
        self.initattr('radial', self.get_root().settings.animation.radial)
        self.initattr('radial_precision', self.get_root().settings.animation.radial_precision)
        self.initattr('framerate', self.get_root().settings.animation.framerate)
        self.initattr('fixed_frames', 0)
        self.initattr('velocity_frames', 0)
        self.initattr('frame_types', defaultdict(lambda: 'fixed', {}))
        self.initattr('heading', None)
        self.initattr('animations', {
            'idle': {
                'E': [0],
                'SE': [0],
                'S': [0],
                'SW': [0],
                'W': [0],
                'NW': [0],
                'N': [0],
                'NE': [0],
            }
        })

        super().fit()
        self.get_root().events.connect('on_key_pressed', 'move_up', f'{self.get_path()}/move_up')
        self.get_root().events.connect('on_key_pressed', 'move_left', f'{self.get_path()}/move_left')
        self.get_root().events.connect('on_key_pressed', 'move_right', f'{self.get_path()}/move_right')
        self.get_root().events.connect('on_key_pressed', 'move_down', f'{self.get_path()}/move_down')
        self.get_root().events.connect('on_key_pressed', 'look_up', f'{self.get_path()}/look_up')
        self.get_root().events.connect('on_key_pressed', 'look_left', f'{self.get_path()}/look_left')
        self.get_root().events.connect('on_key_pressed', 'look_right', f'{self.get_path()}/look_right')
        self.get_root().events.connect('on_key_pressed', 'look_down', f'{self.get_path()}/look_down')
        self.get_root().events.connect('on_key_pressed', 'look_center', f'{self.get_path()}/look_center')

        self.get_root().events.connect('on_key_pressed', 'look_up_left', f'{self.get_path()}/look_up_left')
        self.get_root().events.connect('on_key_pressed', 'look_up_right', f'{self.get_path()}/look_up_right')
        self.get_root().events.connect('on_key_pressed', 'look_down_left', f'{self.get_path()}/look_down_left')
        self.get_root().events.connect('on_key_pressed', 'look_down_right', f'{self.get_path()}/look_down_right')

        self.frame_types = {
            'idle': 'fixed',
            'moving': 'velocity',
        }
        self.set_index(168)
        self.sync_position()

    def set_radial(self, vector):
        x, y = round(vector[0], self.radial_precision), round(vector[1], self.radial_precision)

        if x > 0 and y < 0:
            self.radial = 'NE'
        elif x > 0 and y > 0:
            self.radial = 'SE'
        elif x < 0 and y > 0:
            self.radial = 'SW'
        elif x < 0 and y < 0:
            self.radial = 'NW'
        elif x == 0 and y < 0:
            self.radial = 'N'
        elif x > 0 and y == 0:
            self.radial = 'E'
        elif x == 0 and y > 0:
            self.radial = 'S'
        elif x < 0 and y == 0:
            self.radial = 'W'

    def handle_frames(self):
        self.fixed_frames += self.get_root().delta
        self.velocity_frames += self.get_root().delta*self.velocity.length

    def state_trigger(self):
        if self.state != self.previous_state:
            self.previous_state = self.state
            return True
        return False

    def sync_position(self):
        self.position -= self.get_body_offset()

    def get_body_offset(self):
        return Vector(
            self.position.x - self.body.position.x,
            self.position.y - self.body.position.y
        )

    def set_heading(self, heading: float = None):
        self.heading = heading

    def handle_direction(self):
        if 'W' in self.radial:
            self.direction = 'W'
            self.mirror()
        elif 'E' in self.radial:
            self.direction = 'E'
            self.reset()

    def handle_animation(self):
        self.set_radial(self.motion)
        if self.radial_trigger.handle():
            self.handle_direction()

        animation = self['/cache']['character']['animations'][self.get_state()][self.direction]
        frame_index = int(
            (getattr(self, f'{self.frame_types[self.state]}_frames') / self.framerate) % len(animation)
        )
        self.set_index(animation[frame_index])

    def get_state(self) -> str:
        if self.motion.length > 0.1:
            return 'moving'
        else:
            return 'idle'

    def move_up(self):
        self.motion += Vector(0, (-self.acceleration*self.stats.get_speed()) * self.get_root().delta)

    def move_left(self):
        self.motion += Vector((-self.acceleration*self.stats.get_speed()) * self.get_root().delta, 0)

    def move_right(self):
        self.motion += Vector((self.acceleration*self.stats.get_speed()) * self.get_root().delta, 0)

    def move_down(self):
        self.motion += Vector(0, (self.acceleration*self.stats.get_speed()) * self.get_root().delta)

    def look_up(self):
        self.set_heading((3*pi)/2)

    def look_up_left(self):
        self.set_heading((4*pi)/3)

    def look_left(self):
        self.set_heading(pi)

    def look_right(self):
        self.set_heading(0)

    def look_up_right(self):
        self.set_heading((7*pi)/4)

    def look_down(self):
        self.set_heading(pi/2)

    def look_down_left(self):
        self.set_heading((3*pi)/4)

    def look_down_right(self):
        self.set_heading(pi/4)

    def look_center(self):
        self.set_heading(None)

    def lock_body_rotation(self):
        self.angle = 0.0

    def handle_motion(self):
        if self.motion.length > 0:
            acceleration_vector = self.motion.normalized() * (
                self.acceleration * self.stats.get_speed() * self['/delta']
            )
            self.motion -= acceleration_vector
            self.impulse((acceleration_vector.x, acceleration_vector.y))
            if self.motion.length <= acceleration_vector.length:
                self.motion = Vector(0, 0)

    async def loop(self):
        self.lock_body_rotation()
        self.handle_frames()
        self.handle_animation()
        self.sync_position()
        self.handle_motion()
        await super().loop()
