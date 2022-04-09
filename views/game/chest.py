from collections import defaultdict
from pymunk.vec2d import Vec2d as Vector

from core.body import Body
from core.sprite import Sprite


class Chest(Body, Sprite):
    body_type = 'static'
    vertices = [[-6, -4], [6, -4], [16, -2], [16, 16], [-16, 16], [-16, -2]]
    frames: int = None
    framerate: int = None
    state: str = None
    previous_state: str = None
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
    index = 1

    def build(self):
        self(
            self.name,
        )
        super().build()

    def fit(self):
        self.initattr('actions', [
            {
                'title': 'Loot',
            }
        ])
        self.initattr('state', 'idle')
        self.initattr('framerate', self.get_root().settings.animation.framerate)
        self.initattr('fixed_frames', 0)
        self.initattr('frame_types', defaultdict(lambda: 'fixed', {}))
        self.initattr('animations', {
            'idle': {
            }
        })

        super().fit()
        self.set_frame(595)

        self.frame_types = {
        }
        self.sync_position()

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

    def handle_animation(self):
        self.set_frame(595)

    def get_state(self) -> str:
        ...

    def lock_body_rotation(self):
        self.angle = 0.0

    def set_focused(self):
        self.state = 'focused'

    def set_idle(self):
        self.state = 'idle'

    def handle_focused(self):
        self.draw_outline = True

    def handle_idle(self):
        if self.rect.collidepoint(self['/cursor/position'] + self.offset):
            if self.rect.collidepoint(self['/cursor/left'] + self.offset):
                self['../../../../hud/focus_bar/set_target']({
                    'name': 'Chest',
                    'pointer': self.get_path(),
                    'actions': self.actions,
                })

            self.draw_outline = True
        else:
            self.draw_outline = False

    async def loop(self):
        self.sync_position()
        self[f'handle_{self.state}']()
        await super().loop()
