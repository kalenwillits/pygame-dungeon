from collections import defaultdict
from core.body import Body
from core.sprite import Sprite
from pygame.math import Vector2 as Vector


class Actor(Body, Sprite):
    state: str = None
    previous_state: str = None
    radial: str = None
    heading: float = None  # Intended direction in radians
    previous_radial: str = None
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

    def handle_animation(self):
        ...

    def handle_state(self):
        ...

    def handle_frames(self):
        self.fixed_frames += self.get_root().delta
        self.velocity_frames += self.get_root().delta*self.velocity.length

    def radial_trigger(self):
        if self.radial != self.previous_radial:
            self.previous_radial = self.radial
            return True
        return False

    def state_trigger(self):
        if self.state != self.previous_state:
            self.previous_state = self.state
            return True
        return False

    def sync_position(self):
        self.position -= self.get_body_offset()

    def get_body_offset(self):
        return Vector(
            int(self.position.x - self.body.position.x),
            int(self.position.y - self.body.position.y)
        )

    def set_heading(self, heading: float = None):
        if heading is None:
            self.heading = self.velocity.angle
        else:
            self.heading = heading

    def fit(self):
        self.initattr('state', self.get_root().settings.animation.state)
        self.initattr('radial', self.get_root().settings.animation.radial)
        self.initattr('radial_precision', self.get_root().settings.animation.radial_precision)
        self.initattr('framerate', self.get_root().settings.animation.framerate)
        self.initattr('fixed_frames', 0)
        self.initattr('velocity_frames', 0)
        self.initattr('frame_types', defaultdict(lambda: 'fixed', {}))
        self.initattr('heading', 0.0)
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
        self.sync_position()

    async def loop(self):
        self.sync_position()
        await super().loop()
