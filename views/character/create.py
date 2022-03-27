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

CHARACTER_INIT = {
    'name': None,
    'classe': None,
    'sex': 'male',
}

ANIMATIONS = {
    'warrior': {
        'male': {
            'idle': {
                'W': [119],
                'E': [104],
            },
            'moving': {
                'W': [112, 113, 114, 114],
                'E': [109, 110, 111, 110],
            }
        },
        'female': {
            'idle': {
                'W': [87],
                'E': [72],
            },
            'moving': {
                'W': [82, 81, 80, 81],
                'E': [77, 78, 79, 78],
            }
        }
    },
    'mage': {
        'male': {
            'idle': {
                'W': [183],
                'E': [168],
            },
            'moving': {
                'W': [180, 179, 178, 179],
                'E': [171, 172, 173, 172],
            }
        },
        'female': {
            'idle': {
                'W': [151],
                'E': [136],
            },
            'moving': {
                'W': [148, 147, 146, 147],
                'E': [139, 140, 141, 140],
            }
        }
    },
    'rogue': {
        'male': {
            'idle': {
                'W': [55],
                'E': [40],
            },
            'moving': {
                'W': [50, 49, 48, 49],
                'E': [45, 46, 47, 46],
            }
        },
        'female': {
            'idle': {
                'W': [23],
                'E': [8],
            },
            'moving': {
                'W': [18, 17, 16, 17],
                'E': [13, 14, 15, 14],
            }
        }
    },
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
        def on_press(self):
            self['../data']['animations'] = ANIMATIONS[self['../data']['classe']][self['../data']['sex']]
            self['/cache']['character'] = self['../data']
            self['../../set_view'](['character_overview'])
        self(
            self.name,
            Text(
                'text',
                cols=self.cols,
                rows=self.rows,
                col=self.col,
                row=self.row,
                grid=self.grid,
                value='Create',
                anchor=self.anchor,
            ),
            on_press=on_press,
            **STYLE,
        )
        super().build()

    def handle_disabled_state(self):
        if not self['../data']['name']:
            self.set_disabled()
        elif not self['../data']['classe']:
            self.set_disabled()
        else:
            self.set_idle()

    async def loop(self):
        self.handle_disabled_state()
        await super().loop()

# ------------------------------------------------------------------------------------------------------------------ #


class CharacterCreate(Node):
    data: dict = CHARACTER_INIT

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
            ),
            CreateButton(
                'create_button',
                row=9,
            )
        )
        super().build()
