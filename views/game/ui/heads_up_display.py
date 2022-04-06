from core.node import Node

from components.text import Text
from components.button import Button
from core.interface import Interface
# from components.trigger import Trigger


RELATIVE_POINTER = '../camera/collision_layer/map/player/stats/'

ENGINE_VIEWS = ['settings', 'cache', 'style', 'cursor', 'keybinds', 'events', 'tasks']

MENU_GRID = {
    'grid': True,
    'cols': 2,
    'col': 1,
    'rows': 20,
    'size': (300, 15),
}


class InventoryButton(Button):
    def build(self):
        def on_press(self):
            self['../set_view'](['inventory'])

        self(
            self.name,
            Text(
                'text',
                value='Inventory',
                row=4,
                text_size='sm',
                **MENU_GRID,
            ),
            on_press=on_press,
            row=4,
            **MENU_GRID,
        )
        super().build()


class QuitButton(Button):
    def build(self):
        def on_press(self):
            self.get_root().set_view([*ENGINE_VIEWS, 'menu'])
        self(
            self.name,
            Text(
                'text',
                value='Quit',
                row=15,
                text_size='sm',
                **MENU_GRID,
            ),
            on_press=on_press,
            row=15,
            **MENU_GRID,
        )
        super().build()


class Menu(Node):
    def build(self):
        self(
            self.name,
            Node(
                'main_game_menu',
                InventoryButton(
                    'inventory_button',
                ),
                QuitButton(
                    'quit_button',
                ),
            ),
            size=(500, 500),
            cols=2,
            rows=2,
            row=1,
            col=1,
            grid=True,
        )
        super().build()

    def fit(self):
        self.get_root().events.connect('on_key_up', 'toggle_menu', f'{self.get_path()}/toggle_menu')
        super().fit()
        self.set_view([])

    def toggle_menu(self):
        if not self.view:
            self.set_view(['main_game_menu'])
        else:
            self.set_view([])

# --------------------------------------------------------------------------------------------------------------- #


class HeadsUpDisplay(Node):
    index = 10

    def build(self):
        self(
            self.name,
            Menu('game_menu'),
            Text(
                'name_text',
                text_size='xs',
                anchor='topleft'
            ),
            Text(
                'health_text',
                text_size='xs',
                anchor='topleft',
                position=(0, self['/style/text/xs_character_size'][1])
            ),
        )
        super().build()

    def sync_health(self):
        health_value = 'HP: ' + str(
            self[f'{RELATIVE_POINTER}health']) + '/' + str(self[f'{RELATIVE_POINTER}max_health'])

        if health_value != self.health_text.value:
            self.health_text.set_value(health_value)

    def fit(self):
        super().fit()
        self.name_text.value = self['/cache']['character']['name']
        self.sync_health()

    async def loop(self):
        self.sync_health()
        await super().loop()
