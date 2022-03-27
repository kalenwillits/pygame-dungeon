from pygame import mouse
from pygame.math import Vector2 as Vector

from core.node import Node


class Cursor(Node):
    left: Vector = None
    right: Vector = None

    def build(self):
        self(
            self.name,
        )
        super().build()

    def handle_position(self):
        mouse_position = mouse.get_pos()
        scale = self.get_root().settings.scale_factor
        self.position = Vector(mouse_position[0] * scale, mouse_position[1] * scale)

    def fit(self):
        self.initattr('left', Vector())
        self.initattr('right', Vector())
        super().fit()

    def handle_left(self):
        if mouse.get_pressed()[0]:
            self.left = self.position

    def handle_right(self):
        if mouse.get_pressed()[2]:
            self.right = self.position

    async def loop(self):
        self.handle_position()
        self.handle_left()
        self.handle_right()
        await super().loop()
