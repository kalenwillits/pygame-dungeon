from math import cos, sin, atan2, pi
from pygame.math import Vector2 as Vector

from core.object import Object
from core.sprite import Sprite


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

    def handle_panning(self):
        if self.target is not None:
            orbital = self.get_oribital()
            dist_vector = orbital - self.position
            if dist_vector.length() > self.tolerance:
                speed = self.smoothing * self.get_root().delta
                self.position += dist_vector * speed
            else:
                self.position = orbital
            self.offset = self.position - self.center_offset
            self.cascade(f'{self.get_path()}/pan')

    async def loop(self):
        self.cp.position = self.center_offset + self.offset
        self.cam.position = self.position
        self.target_point.position = self.get_oribital()
        self.handle_panning()
        await super().loop()
