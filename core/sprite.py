from math import degrees

from pygame.transform import scale
from pygame.transform import rotate
from pygame.transform import flip
from pygame import Surface
from pygame import Color
from pygame import Rect
from pygame import mask
from pygame.math import Vector2 as Vector
import pygame

from core.object import Object


class Sprite(Object):
    resource: str = None
    draw_sprite: bool = True
    draw_rect: bool = False
    draw_border: bool = False
    draw_outline: bool = False
    outline_color: Color = None
    outline: mask.Mask = None
    outline_width: float = None
    scale: float = None
    sprite: Surface = None
    fill_color: Color = None
    border_color: Color = None
    area: Rect = None
    area_offset: tuple[int, int] = (0, 0)
    index: int = None
    cols: int = 1
    rows: int = 1

    @property
    def index(self) -> int:
        return self.get_index()

    @index.setter
    def index(self, value: int):
        self.set_index(value)

    def fit(self):
        self.initattr('border_color', self.get_root().style.color.border)
        self.initattr('fill_color', self.get_root().style.color.idle)
        self.initattr('scale', self.get_root().settings.sprite.scale)
        self.initattr('outline_color', self.get_root().style.color.outline)
        self.initattr('outline_width', self.get_root().style.outline.width)

        if self.resource:
            self.sprite = self[self.resource].content
            self.scale_and_size()
            self.area = Rect(0, 0, self.size[0] * self.scale, self.size[1] * self.scale)
            self.build_outline()
            self.rect.size = self.size[0] * self.scale, self.size[1] * self.scale
        super().fit()

    def build_outline(self):
        self.outline = mask.from_surface(self.sprite).to_surface()
        self.outline.set_colorkey((0, 0, 0))
        self.outline.fill(self.outline_color, special_flags=pygame.BLEND_RGBA_MULT)

    def set_index(self, index: int):
        self.area.topleft = (
                (self.size[0] * (index % self.cols)) + self.area_offset[0],
                (self.size[1] * (index // self.cols)) + self.area_offset[1]
        )

    def get_index(self) -> int:
        return int((
            (
                (self.area.topleft[0] - self.area_offset[0]) / (self.size[0] * self.scale)) * self.cols
            ) + (
                (self.area.topleft[1] - self.area_offset[1]) / (self.size[1] * self.scale)
        ))

    def get_sprite_offset(self) -> Vector:
        '''
        Returns the position for the sprite according to the anchor and rect size
        '''
        return {
            'center': Vector(self.rect.center) - Vector(self.size) / 2,
            'top': Vector(self.rect.center[0] - int(self.size[0] / 2), self.rect.top),
            'topleft': Vector(self.rect.topleft),
            'left': Vector(self.rect.left, self.rect.centery - int(self.size[1] / 2)),
            'bottomleft': Vector(self.rect.left, self.rect.bottom - self.size[1]),
            'bottom': Vector(self.rect.centerx - int(self.size[0] / 2), self.rect.bottom - self.size[1]),
            'bottomright': Vector(self.rect.centerx - int(self.size[0] / 2), self.rect.bottom - self.size[1]),
            'right': Vector(self.rect.right - self.size[0], self.rect.centery - int(self.size[1] / 2)),
            'topright': Vector(self.rect.right - self.size[0], self.rect.top),
        }[self.anchor]

    def scale_and_size(self):
        self.sprite = scale(
            self.sprite,
            (
                self.size[0] * self.scale * self.cols,
                self.size[1] * self.scale * self.rows
            )
        )

        offset = self.get_sprite_offset()
        if self.anchor in ('left', 'right'):
            self.rect = self.sprite.get_rect(**{
                self.anchor: offset[0],
                'centery': offset[1],
                'width': self.size[0],
                'height': self.size[1],
            })
        elif self.anchor in ('top', 'bottom'):
            self.rect = self.sprite.get_rect(**{
                self.anchor: offset[1],
                'centerx': offset[0],
                'width': self.size[0],
                'height': self.size[1],
            })
        else:
            self.rect = self.sprite.get_rect(**{
                self.anchor: offset,
                'width': self.size[0],
                'height': self.size[1],
            })

    def rotate(self, angle: float):
        '''
        Rotates the sprite around it's center
        This will rotate the entire sprite image and will not work well on sprite sheets.
        :angle: angle of rotation counter clockwise in radians
        '''
        self.sprite = rotate(self[self.resource].content, degrees(angle))
        self.scale_and_size()

    def mirror(self, x: bool = True, y: bool = False):
        self.sprite = flip(self[self.resource].content, x, y)
        self.scale_and_size()

    def reset(self):
        self.sprite = self[self.resource].content
        self.scale_and_size()

    async def draw(self):
        self.get_root().render(self, fill_color=self.fill_color, border_color=self.border_color)
        await super().draw()
