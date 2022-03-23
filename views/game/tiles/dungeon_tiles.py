from core.sprite import Sprite
from core.body import Body
from core.node import Node

from random import choice


class Floor(Sprite):
    sort = 1

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
    sort = 1

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


class TopWallEdge(Sprite):
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


class BottomWallEdge(Node):
    sort = -1

    def build(self):
        self(
            self.name,
            Body(
                'body',
                body_type='static',
                vertices=[[0, 32], [16, 32], [20, 24], [0, 24]],
                size=(16, 16),
                position=self.position,
            ),
            Floor(
                'floor',
                position=self.position,
            ),
            TopWallEdge(
                'wall_edge',
                position=self.position
            )
        )
        super().build()

    def fit(self):
        super().fit()


TILESET = {
    0: Node,
    1: Floor,
    2: TopWall,
    3: TopWallEdge,
    4: BottomWallEdge,
}
