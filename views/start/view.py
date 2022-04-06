from components.text import Text
from core.interface import Interface
from core.object import Object

from components.detail_card import DetailCard

GRID = {
    'grid': True,
    'rows': 5,
    'cols': 2,
}

ENGINE_VIEWS = ['settings', 'cache', 'style', 'cursor', 'keybinds', 'events', 'tasks']


class Start(Object):
    def build(self):
        self(
            self.name,
            Interface(
                'padding',
                Text(
                    'title_text',
                    value='Mini Dungeon',
                    text_size='lg',
                    row=2,
                    **GRID
                ),
                draw_rect=False,
                size=(500, 100),
                row=2,
                **GRID
            ),
            Text(
                'sub_text',
                value='- Press Enter -',
                text_size='sm',
                anchor='center',
                row=3,
                **GRID,
            ),
            DetailCard(
                'test_detail',
                size=(100, 100),
                card_size=(500, 500),
                title='Test Title',
                body='This is a test\nDamage 20-40\nStrength + 2 awpidhawpidhawpidha awodihawdioh pawdhoawih pwadhaiwodhap awpdihawpidh awdpojwadopj aw[djawdpo awpdoawpod awpodjawpdo aawjdpawodwpaodhapwdhapwdhawpidhawpidhapwidhawpdhwapdhawoawdbawidubawiudgawiduvawidvawidyvawidyvawdiayvwdkuawtdcvawudtcawodutvaodytvaseofuyvaseofuyvasefuoyavsfsaufyvaeifgwvefio32il3fb2l3fvb2lfjvh23f',
                col=1,
                row=2,
                border_color=(0, 0, 200),
                **GRID,
            )
        )
        super().build()

    def fit(self):
        self['../..'].set_view(['menu', *ENGINE_VIEWS])
        self['..'].set_view(['start'])
        self.get_root().events.connect('on_key_down', 'enter', f'{self.get_path()}/close')
        super().fit()

    def close(self):
        self.get_root().events.disconnect('on_key_down', 'enter')
        self['..'].set_view(['character_overview'])
