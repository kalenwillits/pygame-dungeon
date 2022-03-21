from pygame import Rect
from pygame.math import Vector2 as Vector

from core.node import Node


ANCHORS = {
        'center': 'center',
        'left': 'left',
        'right': 'right',
        'top': 'top',
        'bottom': 'bottom',
        'topleft': 'topleft',
        'topright': 'topright',
        'bottomleft': 'bottomleft',
        'bottomright': 'bottomright',
    }


class Object(Node):
    rect: Rect = None
    anchor: str = 'center'
    offset: Vector = None
    area: Rect = None

    def __init__(self, name: str, *children, **kwargs):
        self.rect = Rect(kwargs.get('position', (0, 0)), kwargs.get('size', (0, 0)))
        super().__init__(name, *children, **kwargs)

    def __call__(self, name: str, *children, **kwargs):
        self.rect = Rect(kwargs.get('position', self.position), kwargs.get('size', self.size))
        super().__call__(name, *children, **kwargs)

    @property
    def size(self) -> tuple[int, int]:
        return self.rect.size

    @size.setter
    def size(self, value: tuple[int, int]):
        self.rect.size = value

    @property
    def position(self) -> Vector:
        return getattr(self, f'_{ANCHORS[self.anchor]}')

    @position.setter
    def position(self, value: Vector):
        setattr(self, f'_{ANCHORS[self.anchor]}', value)

    @property
    def _center(self) -> Vector:
        return Vector(self.rect.center)

    @_center.setter
    def _center(self, value: Vector):
        setattr(self.rect, 'center', value)

    @property
    def _top(self) -> Vector:
        return Vector(self.rect.top, self.rect.centery)

    @_top.setter
    def _top(self, value: Vector):
        setattr(self.rect, 'centerx', value[0])
        setattr(self.rect, 'top', value[1])

    @property
    def _topleft(self) -> Vector:
        return Vector(self.rect.topleft)

    @_topleft.setter
    def _topleft(self, value: Vector):
        setattr(self.rect, 'topleft', value)

    @property
    def _left(self) -> Vector:
        return Vector(self.rect.left, self.rect.centery)

    @_left.setter
    def _left(self, value: Vector):
        setattr(self.rect, 'left', value[0])
        setattr(self.rect, 'centery', value[1])

    @property
    def _bottomleft(self) -> Vector:
        return Vector(self.rect.bottomleft)

    @_bottomleft.setter
    def _bottomleft(self, value: Vector):
        setattr(self.rect, 'bottomleft', value)

    @property
    def _bottom(self) -> Vector:
        return Vector(self.rect.bottom)

    @_bottom.setter
    def _bottom(self, value: Vector):
        setattr(self.rect, 'centerx', value[0])
        setattr(self.rect, 'bottom', value[1])

    @property
    def _bottomright(self) -> Vector:
        return Vector(self.rect.bottomright)

    @_bottomright.setter
    def _bottomright(self, value: Vector):
        setattr(self.rect, 'bottomright', value)

    @property
    def _right(self) -> Vector:
        return Vector(self.rect.right)

    @_right.setter
    def _right(self, value: Vector):
        setattr(self.rect, 'right', value[0])
        setattr(self.rect, 'centery', value[1])

    @property
    def _topright(self) -> Vector:
        return Vector(self.rect.topright)

    @_topright.setter
    def _topright(self, value: Vector):
        setattr(self.rect, 'topright', value)

    def get_rect_params(self):
        if self.anchor in ('center', 'topleft', 'bottomright', 'bottomleft', 'topright'):
            return {self.anchor: self.position}
        elif self.anchor in ('left', 'right'):
            return {self.anchor: self.position[0], 'centery': self.position[1]}
        elif self.anchor in ('top', 'bottom'):
            return {'centerx': self.position[0], self.anchor: self.position[1]}

    def fit(self):
        self.initattr('offset', Vector())
        super().fit()

    def build(self):
        self.initattr('anchor', 'center')
        self.initattr('size', self.get_root().style.rect.size)
        self.initattr('offset', Vector())
        super().build()
