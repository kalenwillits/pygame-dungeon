from pygame import mouse
from pygame.math import Vector2 as Vector

from core.node import Node


class Cursor(Node):
    # TODO - Play with creating custom cursors. https://www.pygame.org/docs/ref/cursors.html#pygame.cursors.cursor

    def handle_position(self):
        mouse_position = mouse.get_pos()
        scale = self.get_root().settings.scale_factor
        self.position = Vector(mouse_position[0] * scale, mouse_position[1] * scale)

    async def loop(self):
        self.handle_position()
        await super().loop()
