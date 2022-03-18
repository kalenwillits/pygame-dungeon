from components.text import Text
from core.object import Object

from .style import GRID
from .character_select_button import CharacterSelectButton
from .status_text import StatusText


class CharacterSelectView(Object):
    def fit(self):
        # self.get_root().events.connect('on_key_down', 'enter', f'{self.get_path()}/close')
        super().fit()


character_select = CharacterSelectView(
    'character_select',
    CharacterSelectButton(
        'character_select_button',
        row=3,
    ),
    StatusText(
        'status_text',
        row=4,
        **GRID,
    ),
)
