from components.text import Text
from components.button import Button
from components.trigger import Trigger

from core.node import Node

GRID = {
    'grid': True,
    'cols': 2,
    'rows': 7,
}
BUTTON = {
    'size': (300, 30),
}

STATIC_VIEWS = {'quit_button', 'settings_button'}

CHARACTER_CREATED_VIEW = {'character_button', *STATIC_VIEWS}
CHARACTER_NOT_CREATED_VIEW = {'character_create_button', *STATIC_VIEWS}


class CharacterButton(Button):
    def build(self):
        self(
            self.name,
            Text(
                'text',
                **self.kwargs
            ),
        )
        super().build()

    def handle_populate(self):
        if self.get_root().data.get('character') is not None:
            self.text.value = self.get_root().data.get('character', {}).get('name', '')

    async def loop(self):
        if self['../character_trigger'].handle():
            self.handle_populate()
        await super().loop()


class SettingsButton(Button):
    def build(self):
        self(
            self.name,
            Text(
                'text',
                value='Settings',
                **self.kwargs,
            )
        )
        super().build()


class QuitButton(Button):
    def build(self):
        self(
            self.name,
            Text(
                'text',
                value='Quit',
                **self.kwargs,
            ),
            on_press=self.handle_quit,
        )
        super().build()

    @staticmethod
    def handle_quit(self):
        self.get_root().quit = True


BUTTON_NODES = [
    CharacterButton,
    SettingsButton,
    QuitButton,
]


class MainMenu(Node):
    @property
    def has_character_name(self) -> bool:
        if self.get_root().data.get('character', {}).get('name'):
            return True
        return False

    def build(self):
        self(
            self.name,
            Trigger(
                'character_trigger',
                value='../has_character_name',
            ),
            CharacterButton(
                'character_button',
                row=2,
                **GRID,
                **BUTTON,
            ),
            SettingsButton(
                'settings_button',
                row=3,
                **GRID,
                **BUTTON,
            ),
            QuitButton(
                'settings_button',
                row=4,
                **GRID,
                **BUTTON,
            ),

        )
        super().build()

    async def loop(self):
        if self.character_trigger.handle():
            self.handle_view()
        await super().loop()

    def handle_view(self):
        if self.get_root().data.get('character') is not None:
            self.set_view(CHARACTER_CREATED_VIEW)
        else:
            self.set_view(CHARACTER_NOT_CREATED_VIEW)
