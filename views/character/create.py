import re

from core.node import Node
from components.button import Button
from components.text import Text
from components.input import Input


STYLE = {
    'cols': 2,
    'rows': 12,
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


class ClasseRadial(Node):
    style = {
        'cols': 6,
        'rows': STYLE['rows'],
        'grid': True,
        'size': (75, 20),
    }

    def build(self):
        def on_press(self):
            for child in self['../get_children']():
                if child.name != self.name:
                    self[f'../{child.name}/set_idle']()
                else:
                    self['../../data']['classe'] = self.name

        def on_release(self):
            if not any([child.state == 'pressed' for child in self['../get_children']()]):
                self['../../data']['classe'] = None

        self(
            self.name,
            Button(
                'warrior',
                Text(
                    'text',
                    value='Warrior',
                    col=2,
                    row=self.row,
                    **self.style,
                ),
                is_toggle=True,
                col=2,
                row=self.row,
                on_press=on_press,
                on_release=on_release,
                **self.style,
            ),
            Button(
                'rogue',
                Text(
                    'text',
                    value='Rogue',
                    col=3,
                    row=self.row,
                    **self.style,
                ),
                is_toggle=True,
                col=3,
                row=self.row,
                on_press=on_press,
                on_release=on_release,
                **self.style,
            ),
            Button(
                'mage',
                Text(
                    'text',
                    value='Mage',
                    col=4,
                    row=self.row,
                    **self.style,
                ),
                is_toggle=True,
                col=4,
                row=self.row,
                on_press=on_press,
                on_release=on_release,
                **self.style,
            ),

        )
        super().build()


class NameInput(Input):
    def build(self):
        def on_change(self):
            previous_length = len(self.value)
            self.value = re.sub(r'[^a-zA-Z]', '', self.value)
            self.cursor_position -= (previous_length - len(self.value))
            self['../data']['name'] = self.value

        self(
            self.name,
            on_change=on_change,
            max_characters=24,
            **STYLE,
        )
        super().build()


class CreateButton(Button):
    def build(self):
        self(
            self.name,
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
                row=6,
            ),
            ClasseRadial(
                'classe_radial',
                row=7,
            ),
            NameInput(
                'name_input',
                row=8,
            )
        )
        super().build()

    def fit(self):
        super().fit()

    async def loop(self):
        await super().loop()

    async def draw(self):
        await super().draw()
