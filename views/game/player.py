from math import pi
from core.actor import Actor

from pymunk.vec2d import Vec2d as Vector


class Player(Actor):
    vertices = [[-10, 30], [-10, 6], [2, 0], [12, 6], [12, 30]]
    level: int = 1
    animations = {
        'idle': {
            'W': [*[183 for _ in range(30)], 182, 181, 182],
            'E': [*[168 for _ in range(30)], 169, 170, 169]
        },
        'moving': {
            'W': [180, 179, 178, 179],
            'E': [171, 172, 173, 172]
        }
    }
    direction: str = 'E'

    def fit(self):
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

    def build(self):
        self(
            self.name,
        )
        super().build()

    def handle_direction(self):
        if 'W' in self.radial:
            self.direction = 'W'
            self.mirror()
        elif 'E' in self.radial:
            self.direction = 'E'
            self.reset()

    def handle_animation(self):
        self.set_radial(self.velocity)
        if self.radial_trigger.handle():
            self.handle_direction()

        animation = self.animations[self.get_state()][self.direction]
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

    def move_left(self):
        force = Vector(-self.acceleration * self.get_root().delta, 0)
        self.impulse(force)

    def move_right(self):
        force = Vector(self.acceleration * self.get_root().delta, 0)
        self.impulse(force)

    def move_down(self):
        force = Vector(0, self.acceleration * self.get_root().delta)
        self.impulse(force)

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

    async def loop(self):
        self.lock_body_rotation()

        self.handle_frames()
        self.handle_animation()
        await super().loop()

