from components.text import Text
from core.interface import Interface
from core.object import Object

from components.paragraph import Paragraph

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
            Paragraph(
                'test_para',
                size=(200, 200),
                value="""
                THIS IS A TEST
                BEEP
                BEEP
                BEEP
                GIWAWOGIHAWGOUAWGH{AWOGUHAWGO{UHAWGOAWGUH"AOWGHAW"GOAWHG"OAWIGH"AWGOIHAW"OGIHAWG"OAWIGHAWOGHAWG:AWGH
                """,
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
