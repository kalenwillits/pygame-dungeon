from core.node import Node
from components.button import Button
from components.text import Text


STYLE = {
    'cols': 2,
    'rows': 8,
    'col': 1,
    'grid': True,
    'size': (250, 20),
}


class SexButton(Button):
    is_toggle = True

    def build(self):

        def on_press(self):
            self.text.set_value('Female')
            self['../data']['sex'] = 'female'

        def on_release(self):
            self.text.set_value('Male')
            self['../data']['sex'] = 'male'

        self(
            self.name,
            Text(
                'text',
                cols=self.cols,
                rows=self.rows,
                col=self.col,
                row=self.row,
                grid=self.grid,
                value='Male',
                anchor=self.anchor,
            ),
            on_press=on_press,
            on_release=on_release,
            **STYLE,
        )
        super().build()

# ------------------------------------------------------------------------------------------------------------------ #


class CharacterCreate(Node):
    data: dict = {
        'name': None,
        'classe': None,
        'sex': 'male',
    }

    def build(self):
        self(
            self.name,
            SexButton(
                'sex_button',
                row=5,
            )
        )
        super().build()

    def fit(self):
        super().fit()

    async def loop(self):
        await super().loop()

    async def draw(self):
        await super().draw()
