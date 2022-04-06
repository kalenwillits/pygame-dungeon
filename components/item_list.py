from core.interface import Interface
from components.text import Text

from pygame.math import Vector2 as Vector


class Item(Interface):
    draw_border = False
    index: int = None

    @property
    def value(self) -> str:
        return self.text.value

    @value.setter
    def value(self, value: str):
        self.text.value = value

    def sync_position(self):
        self.text.position = self.position

    def build(self):
        self(
            self.name,
            Text(
                'text',
                anchor='left',
                text_size='xs',
            ),
            anchor='left',
        )
        super().build()

    async def loop(self):
        self.sync_position()
        await super().loop()


class ItemSchema(dict):
    value: str
    on_hover: str

# ------------------------------------------------------------------------------------------------------------ #


class ItemList(Interface):
    item_list: list[ItemSchema] = None
    scroll: float = None

    def build(self):
        self(
            self.name,
        )
        super().build()

    def fit(self):
        self.initattr('scroll', 0.0)
        self.initattr('item_list', [])
        super().fit()

    def build_items(self):
        for index, item in enumerate(self.item_list):
            self(
                self.name,
                Item(
                    f'item_{index}',
                    value=item.value,
                    position=Vector(self.rect.left, self.rect.top + self['style/text/xs_character_size'] * index),
                    index=index,
                    )
                )
