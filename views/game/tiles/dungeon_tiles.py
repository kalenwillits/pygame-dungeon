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
            vertices=[[24, -8], [24, -2], [-8, -2], [-8, -8]]
        )

    def fit(self):
        super().fit()
        self.set_index(34)


class TopLeftWall(Body, Sprite):
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
            vertices=[[-8, -8], [24, -8], [24, -2], [0, -2], [0, 24], [-8, 24]]
        )

    def fit(self):
        super().fit()
        self.set_index(258)


class TopRightWall(Body, Sprite):
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
            vertices=[[-8, -2], [16, -2], [16, 24], [24, 24], [24, -8], [-8, -8]],
        )

    def fit(self):
        super().fit()
        self.set_index(259)


class LeftWall(Body, Sprite):
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
            vertices=[[-8, -8], [0, -8], [0, 24], [-8, 24]]
        )

    def fit(self):
        super().fit()
        self.set_index(257)


class RightWall(Body, Sprite):
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
            vertices=[[16, -8], [16, 24], [24, 24], [24, -8]]
        )

    def fit(self):
        super().fit()
        self.set_index(256)


class BottomLeftWallEdge(Body, Sprite):
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
            vertices=[[0, -8], [0, 24], [-8, 24], [-8, -8]]
        )

    def fit(self):
        super().fit()
        self.set_index(290)


class BottomLeftWall(Body, Sprite):
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
            vertices=[[-2, -8], [-2, 18], [24, 18], [24, 24], [-8, 24], [-8, -8]]
        )

    def fit(self):
        super().fit()
        self.set_index(322)


class BottomRightWall(Body, Sprite):
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
            vertices=[[-8, 18], [16, 18], [16, -8], [24, -8], [24, 24], [-8, 24]]
        )

    def fit(self):
        super().fit()
        self.set_index(323)


class BottomRightWallEdge(Body, Sprite):
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
            vertices=[[16, -8], [16, 24], [24, 24], [24, -8]]
        )

    def fit(self):
        super().fit()
        self.set_index(291)


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
            vertices=[[24, 18], [-8, 18], [-8, 24], [24, 24]]
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


class TopLeftWallEdge(Sprite):
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
        self.set_index(226)


class TopRightWallEdge(Sprite):
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
        self.set_index(227)


class PillarBase(Sprite):
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
        )

    def fit(self):
        super().fit()
        self.set_index(229)


class PillarMid(Body, Sprite):
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
            vertices=[[18, -12], [18, 10], [14, 14], [4, 14], [-2, 10], [-2, -12]]
        )

    def fit(self):
        super().fit()
        self.set_index(197)


class PillarTop(Sprite):
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
        )

    def fit(self):
        super().fit()
        self.set_index(165)


TILESET = {
    0: Node,
    1: Floor,
    2: TopWall,
    3: WallEdge,
    4: BottomWall,
    5: TopLeftWall,
    6: TopLeftWallEdge,
    7: LeftWall,
    8: BottomLeftWall,
    9: BottomLeftWallEdge,
    10: BottomRightWall,
    11: BottomRightWallEdge,
    12: RightWall,
    13: TopRightWall,
    14: TopRightWallEdge,
    15: PillarBase,
    16: PillarMid,
    17: PillarTop,
}
