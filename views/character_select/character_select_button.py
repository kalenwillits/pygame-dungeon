from components.button import Button
from components.text import Text

from .style import GRID


class CharacterSelectButton(Button):
    def build(self):
        self(
            self.name,
            Text(
                'text',
                value='+',
                **GRID,
                row=self.row,
                col=self.col,
            ),
            size=(200, 200),
            **GRID,
        )
        super().build()
