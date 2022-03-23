from core.sprite import Sprite
from core.body import Body
from core.node import Node

from random import choice


class FloorTile(Sprite):
    def build(self):
        self(
            self.name,
            anchor='topleft',
            size=(16, 16),
            cols=32,
            rows=32,
            resource='/resources/spritesheet',
            draw_border=True,
            border_radius=0,
            border_width=3,
            border_color=(0, 0, 255)
        )

        super().build()

    def fit(self):
        super().fit()
        self.set_index(choice([129, 130, 131, 161, 162, 163]))


class VerticalWallEdgeTile(Sprite):
    sort = 1

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


class VerticalWallEdgeWithFloorTile(VerticalWallEdgeTile):
    sort = 2

    def build(self):
        self(
            self.name,
            FloorTile(
                'floor',
            )
        )


class VerticalWallTile(Body, Sprite):
    def build(self):
        self(
            self.name,
            body_type='static',
            anchor='topleft',
            size=(16, 16),
            cols=32,
            rows=32,
            resource='../../../../../../resources/spritesheet',
            vertices=[[0, 0], [0, 32], [32, 32], [32, 0]],
        )

    def fit(self):
        super().fit()
        self.set_index(34)


class HorizontalWallTile(Body, Sprite):
    def build(self):
        self(
            self.name,
            body_type='static',
            anchor='topleft',
            size=(16, 16),
            cols=32,
            rows=32,
            resource='/resources/spritesheet',
            vertices=[[-16, -16], [-16, 16], [16, 16], [16, 16]],
            border_radius=0,
        )

    def fit(self):
        super().fit()
        self.set_index(289)


TILESET = {
    0: Node,
    1: FloorTile,
    2: VerticalWallTile,
    3: VerticalWallEdgeTile,
    4: HorizontalWallTile,
    5: VerticalWallEdgeWithFloorTile,
}
