from pygame.math import Vector2 as Vector
from pygame import Surface

from core.sprite import Sprite


class Interface(Sprite):
    row: float = 1.0
    col: float = 1.0
    rows: float = 1.0
    cols: float = 1.0
    grid: bool = False

    sprite: Surface = None

    draw_sprite: bool = True
    draw_rect: bool = True
    draw_border: bool = True

    def fit(self):
        if self.grid:
            self.apply_grid()
        super().fit()

    def apply_grid(self):
        '''
        Grid function to calculate component position based on a grid defined in params.
        Items are placed on the center of the column
        i.e. cols=2 will split the viewport in half and place the center of the item on the split
        '''
        settings = self.get_root().settings
        position_x = ((settings.resolution.x / (self.cols)) * self.col)
        position_y = ((settings.resolution.y / (self.rows)) * self.row)

        self.position = Vector(position_x, position_y)
