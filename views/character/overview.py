from core.node import Node
from components.button import Button
from components.text import Text
from components.trigger import Trigger

STYLE = {
    'cols': 2,
    'rows': 8,
    'col': 1,
    'grid': True,
    'size': (250, 20),
}

ENGINE_VIEWS = ['settings', 'data', 'style', 'cursor', 'keybinds', 'events', 'tasks']


class ActionButton(Button):
    def build(self):
        def on_release(self):
            if self['../character']:
                self['/main/set_view'](['game', *ENGINE_VIEWS])
            else:
                self['../../set_view'](['character_create'])
        self(
            self.name,
            Text(
                'text',
                cols=self.cols,
                rows=self.rows,
                col=self.col,
                row=self.row,
                grid=self.grid,
                value='New',
                anchor=self.anchor,
            ),
            Trigger(
                'character_state_trigger',
                value='../../character',
            ),
            on_release=on_release,
            **STYLE,
        )
        super().build()

    def fit_text_state(self):
        if self['../character']:
            self.text.set_value('Enter')
        else:
            self.text.set_value('New')

    def handle_text_state(self):
        if self.character_state_trigger.handle():
            self.fit_text_state()

    def fit(self):
        self.fit_text_state()
        super().fit()

    async def loop(self):
        self.handle_text_state()
        await super().loop()


class DeleteCharacterButton(Button):
    def build(self):
        def on_release(self):
            self.character = {}
        self(
            self.name,
            Text(
                'text',
                cols=self.cols,
                rows=self.rows,
                col=self.col,
                row=self.row,
                grid=self.grid,
                value='Delete',
                anchor=self.anchor,
            ),
            on_release=on_release,
            **STYLE,
        )
        super().build()


class QuitButton(Button):
    def build(self):

        def on_release(self):
            self['/exit']()

        self(
            self.name,
            Text(
                'text',
                cols=self.cols,
                rows=self.rows,
                col=self.col,
                row=self.row,
                grid=self.grid,
                value='Quit',
                anchor=self.anchor,
            ),
            on_release=on_release,
            **STYLE,
        )
        super().build()

# ------------------------------------------------------------------------------------------------------------------ #


class CharacterOverview(Node):
    def build(self):
        self(
            self.name,
            # Character name and level goes here.
            # Character sprite goes here.
            ActionButton(
                'action_button',
                row=5,
                ),
            DeleteCharacterButton(
                'delete_character_button',
                row=6,
            ),
            QuitButton(
                'quit_button',
                row=7,
            ),
            Trigger(
                'character_state_trigger',
                value='../character',
            ),
        )
        super().build()

    @property
    def character(self) -> dict:
        return self['/data/get']('character')

    def fit_view_state(self):
        if self.character:
            self.set_view(['action_button', 'delete_character_button', 'quit_button'])
        else:
            self.set_view(['action_button', 'quit_button'])

    def handle_view_state(self):
        if self.character_state_trigger():
            self.fit_view_state()

    def fit(self):
        self.fit_view_state()
        super().fit()

    async def loop(self):
        await super().loop()

    async def draw(self):
        await super().draw()
