from pygame.math import Vector2 as Vector

from core.object import Object


class Camera(Object):
    target: str = None

    def fit(self):
        self.initattr('target', None)
        self.initattr('offset', Vector())
        self.initattr('offset_float', Vector())
        self.target = 'collision_layer/player'
        super().fit()
        self.handle_panning()

    def get_target_offset(self):
        return Vector(
            int(
                (self[self.target].position[0] - self.offset_float.x) - self.get_root().settings.resolution[0] / 2
            ),
            int(
                (self[self.target].position[1] - self.offset_float.y) - self.get_root().settings.resolution[1] / 2
            )
        )

    def pan(self, node):
        if isinstance(node, Object):
            node.offset = self.offset

    def handle_panning(self):
        self.offset = self.get_target_offset()
        self.cascade(f'{self.get_path()}/pan')

    async def loop(self):
        self.handle_panning()
        await super().loop()
