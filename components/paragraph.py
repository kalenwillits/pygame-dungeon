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
        value_queue = self.value
        line_number = 0

        while value_queue:
            line = value_queue[:self.line_length]

            if '\n' in line:
                # Line break
                index = line.index('\n')
            elif ' ' in line:
                # word break
                if line[-1] != ' ':
                    index = (len(line) - line[::-1].index(' '))
                else:
                    index = self.line_length
            else:
                index = self.line_length

            if index > 0:
                line = value_queue[:index].replace('\n', '')
                self.add_child(
                    Text(
                        f'{self.name}_{line_number}',
                        text_size=self.text_size,
                        text_color=self.text_color,
                        margin=self.margin,
                        value=line,
                        position=(self.rect.left, self.rect.top + (line_number * self.line_height))
                    )
                )
            else:
                index = 1

            value_queue = value_queue[index:]
            line_number += 1

    async def loop(self):
        if self.value_trigger():
            self.update_value()
        await super().loop()
