from math import cos, sin
from pygame.math import Vector2 as Vector

from core.object import Object


class Camera(Object):
    '''
    Following Camera to scroll with a object node.
    ### Usage
        Place elements that will be within the camera's scope inside the camera.
        Set a `target` param as a relative path to the object being followed.
    '''
    target: str = None
    smoothing: float = None
    lookahead: float = None
    draw_rect: bool = False
    draw_border: bool = False
    draw_outline: bool = False

    def fit(self):
        self.initattr('smoothing', self.get_root().settings.camera.smoothing)
        self.initattr('lookahead', self.get_root().settings.camera.lookahead)
        self.initattr('tolerance', self.get_root().settings.camera.tolerance)
        self.initattr('target', None)
        self.initattr('center_offset', Vector(self.get_root().settings.resolution) / 2)

        super().fit()
        if self.target is not None:
            self.position = self[self.target].position
            self.handle_panning()
            self.reset()

    def get_lookahead_vector(self) -> Vector:
        velocity = self[self.target].velocity
        return self[self.target].position + (int(velocity.x * self.lookahead), int(velocity.y * self.lookahead))

    def get_oribital(self):
        return self[self.target].position + Vector(
            cos(self[self.target].heading),
            sin(self[self.target].heading)
        ) * self.lookahead

    def pan(self, node):
        if isinstance(node, Object):
            node.offset = self.offset

    def reset(self):
        self.position = self[self.target].position

    def handle_panning(self):
        if self.target is not None:
            orbital = self.get_oribital()
            to_orbital_vector = orbital - self.position
            if to_orbital_vector.length() > self.tolerance:
                self.position += to_orbital_vector.normalize() * (self.smoothing) * self.get_root().delta
            else:
                self.position = orbital

            self.offset = self.position - self.center_offset
            self.cascade(f'{self.get_path()}/pan')

    async def loop(self):
        self.handle_panning()
        await super().loop()
