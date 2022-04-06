from pygame import mouse
from pygame.math import Vector2 as Vector

from core.node import Node
from components.trigger import Trigger


class Cursor(Node):
    left: Vector = None
    right: Vector = None
    hover: Vector = None

    hover_counter: float = None
    hover_delay: float = None

    def build(self):
        self(
            self.name,
            Trigger(
                'hover_trigger',
                value='../position',
            ),
        )
        super().build()

    def handle_position(self):
        mouse_position = mouse.get_pos()
        scale = self.get_root().settings.scale_factor
        self.position = Vector(mouse_position[0] * scale, mouse_position[1] * scale)

    def fit(self):
        self.initattr('position', Vector())
        self.initattr('left', Vector())
        self.initattr('right', Vector())
        self.initattr('hover', None)
        self.initattr('hover_counter', 0.0)
        self.initattr('hover_delay', self['/settings/cursor/hover_delay'])
        super().fit()

    def handle_left(self):
        if mouse.get_pressed()[0]:
            self.left = self.position

    def handle_right(self):
        if mouse.get_pressed()[2]:
            self.right = self.position

    def handle_hover(self):
        self.hover_counter += self['/delta']

        if self.hover_trigger.handle():
            self.hover_counter = 0.0
            self.hover = None

        if self.hover_counter > self.hover_delay:
            self.hover = self.position

    async def loop(self):
        self.handle_position()
        self.handle_left()
        self.handle_right()
        self.handle_hover()
        await super().loop()
