from pygame import Color

from core.interface import Interface
from components.text import Text


class Paragraph(Interface):
    value: str = None
    previous_value: str = None
    text_size: str = None
    text_color: Color = None
    margin: float = None
    spacing: float = None

    draw_rect = False
    draw_border = False

    def value_trigger(self) -> bool:
        if self.value != self.previous_value:
            self.previous_value = self.value
            return True
        return False

    def fit(self):
        self.initattr('margin', self['/style/text/margin'])
        self.initattr('text_color', self['/style/color/text'])
        self.initattr('text_size', self['/settings/paragraph/text_size'])
        self.initattr('spacing', self['/settings/paragraph/spacing'])
        self.initattr('value', '')
        super().fit()
        character_size = self[f'/style/text/{self.text_size}'].render(
            '_',
            True,
            self.text_color,
        ).get_size()
        self.line_length = self.size[0] // character_size[0]
        self.line_height = character_size[1] * self.spacing
        self.update_value()

    def update_value(self):
        self.clear_children()
        value_queue = self.value.replace('\n', '')
        line_number = 0
        while value_queue:
            self.add_child(
                Text(
                    f'{self.name}_{line_number}',
                    text_size=self.text_size,
                    text_color=self.text_color,
                    margin=self.margin,
                    value=value_queue[:self.line_length + 1],
                    position=(self.position.x, self.position.y + (line_number * self.line_height))
                )
            )
            value_queue = value_queue[self.line_length:]
            line_number += 1

    async def loop(self):
        if self.value_trigger():
            self.update_value()
        await super().loop()
