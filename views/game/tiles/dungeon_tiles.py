from core.sprite import Sprite
from core.body import Body
from core.node import Node

from random import choice


class Floor(Sprite):
    level = 0

    def build(self):
        self(
            self.name,
            anchor='topleft',
            size=(16, 16),
            cols=32,
            rows=32,
            resource='/resources/spritesheet',
            border_radius=0,
            border_width=3,
            border_color=(0, 0, 255),
        )

        super().build()

    def fit(self):
        super().fit()
        self.set_index(choice([129, 130, 131, 161, 162, 163]))


class TopWall(Body, Sprite):
    level = 0

    def build(self):
        self(
            self.name,
            body_type='static',
            anchor='topleft',
            size=(16, 16),
            cols=32,
            rows=32,
            resource='../../../../../../resources/spritesheet',
            vertices=[[0, 0], [0, 16], [32, 16], [32, 0]],
        )

    def fit(self):
        super().fit()
        self.set_index(34)


class BottomWall(Body, Sprite):
    level = 2

    def build(self):
        self(
            self.name,
            body_type='static',
            anchor='topleft',
            size=(16, 16),
            cols=32,
            rows=32,
            resource='../../../../../../resources/spritesheet',
            vertices=[[0, 0], [0, 16], [32, 16], [32, 0]],
        )

    def fit(self):
        super().fit()
        self.set_index(34)


class WallEdge(Sprite):
    level = 2

    def build(self):
        self(
            self.name,
            body_type='static',
            anchor='topleft',
            size=(16, 16),
            cols=32,
            rows=32,
            resource='/resources/spritesheet',
        )

    def fit(self):
        super().fit()
        self.set_index(2)


TILESET = {
    0: Node,
    1: Floor,
    2: TopWall,
    3: WallEdge,
    4: BottomWall,
}
