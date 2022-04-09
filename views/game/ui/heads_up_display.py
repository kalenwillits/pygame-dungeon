from pygame import mouse

from core.node import Node
from core.interface import Interface

from components.text import Text
from components.button import Button
from components.item_list import ItemList
from components.trigger import Trigger
from components.detail_card import DetailCard


RELATIVE_POINTER = '../camera/collision_layer/map/player/stats/'

ENGINE_VIEWS = ['settings', 'cache', 'style', 'cursor', 'keybinds', 'events', 'tasks']

MENU_GRID = {
    'grid': True,
    'cols': 2,
    'col': 1,
    'rows': 20,
    'size': (300, 15),
}

HUD_BAR = {
    'size': ((16+4)*16, 20),
    'grid': True,
    'rows': 20,
    'cols': 2,
    'col': 1,
    }


class Inventory(ItemList):
    @property
    def items_pointer(self) -> list:
        return self['/cache']['character']['inventory']

    def build(self):
        self(
            self.name,
            items='items_pointer',
            item_size=(192, 15),
            position=(10, -1),
            border_radius=0,
            size=(200, self['/settings/resolution'][1] + 2),
            anchor='topleft',
        )
        super().build()

    def add_item(self, item: dict, index=-1):
        self['/cache']['character']['inventory'].insert(index, item)

    def remove_item(self):
        ...


class InventoryButton(Button):
    def build(self):
        def on_press(self):
            self['../../set_view'](['inventory'])

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


class FocusBar(Interface):
    target: dict = {}

    def get_target(self) -> dict:
        return self.target

    def set_target(self, value: dict):
        self.target = value

    def build(self):
        self(
            self.name,
            Trigger(
                'change_trigger',
                value='../target',
            ),
            Text(
                'text',
                value='',
                cols=self.cols,
                col=self.col,
                rows=self.rows,
                row=self.row,
                grid=self.grid,
            ),
            row=1,
            **HUD_BAR
            )
        super().build()

    def fit(self):
        self['/events/connect']('on_key_up', 'toggle_focus', f'{self.get_path()}/clear_focus')
        super().fit()

    def handle_focus_change(self):
        if self.change_trigger.handle():
            self.text.set_value(self.target.get('name', ''))
            if self.target:
                self[f'/{self.target.get("pointer")}'].set_focused()
                self['../action_bar/set_actions'](self.target.get('actions', []))

    def clear_focus(self):
        if self.target:
            self[f'/{self.target.get("pointer")}'].set_idle()
        self.target = {}
        self.text.set_value('')
        self['/cursor/set_left']((float('inf'), float('inf')))
        self['../action_bar/clear_actions']()

    def toggle_focus(self):
        # TODO search for other things to focus on.
        self.clear_focus()

    async def loop(self):
        self.handle_focus_change()
        await super().loop()


class ActionButton(Button):
    target: str = None

    def build(self):
        def on_press(self):
            self[self.target]()

        self(
            self.name,
            Text(
                'text',
                value=self.value,
                text_size='xs',
                position=self.text_position,
            ),
            DetailCard(
                'detail_card',
                title=self.kwargs.get('title'),
                body=self.kwargs.get('body'),
                card_size=(150, 100),
                card_anchor='bottomleft',
                size=(16, 16),
                anchor='center',
                position=self.position,
                card_position=self.position,
            ),
            on_press=on_press,
            size=(16, 16),
        )
        super().build()


class ActionBar(Interface):
    actions: list[dict] = []
    margin: int = 1

    def build(self):
        self(
            self.name,
            Trigger(
                'change_trigger',
                value='../actions',
            ),
            row=18,
            **HUD_BAR,
        )
        super().build()

    def clear_actions(self):
        self.actions = []

    def set_actions(self, value: list[dict]):
        self.actions = value

    def get_actions(self) -> list[dict]:
        return self.actions

    def build_actions(self):
        for child_name in [child.name for child in self]:
            if 'action' in child_name:
                self.remove_child(child_name)

        for index, option in enumerate(self.actions):

            self.add_child(
                ActionButton(
                    f'action_{index + 1}',
                    position=(
                        ((self.rect.left + self.margin) + (self.rect.left + self.margin) * index) - 7,
                        self.rect.centery - 16,
                    ),
                    text_position=(
                        ((self.rect.left + self.margin) + (self.rect.left + self.margin) * index) + 2,
                        self.rect.centery - 13,
                    ),
                    target=option.get('target', '../change_focus'),
                    value=f'{index + 1}',
                    title=option.get('title'),
                    body=option.get('body'),
                )
            )

    def handle_actions_change(self):
        if self.change_trigger.handle():
            self.build_actions()

    def fit(self):
        self.initattr('actions', [])
        self.build_actions()
        super().fit()

    async def loop(self):
        self.handle_actions_change()
        await super().loop()


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
            Inventory('inventory'),
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
            FocusBar('focus_bar'),
            ActionBar('action_bar'),
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
