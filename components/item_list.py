from core.interface import Interface
from components.text import Text
from components.trigger import Trigger

ITEM_SCHEMA = {
    'title': str,
    'body': str,
}


class Item(Interface):
    margin: float = None

    draw_border = False

    def build(self):
        self(
            self.name,
            Text(
                'item_name_text',
                value=self.kwargs.get('title'),
                anchor='left',
                text_size='xs',
            ),
            anchor='topleft',
        )
        super().build()

    def place_content(self):
        self.item_name_text.position = self.rect.left + self.margin, self.rect.centery

    def fit(self):
        self.initattr('margin', 4)
        super().fit()
        self.place_content()

    def handle_focus(self):
        if self.rect.collidepoint(self['/cursor/position']):
            self.draw_border = True
        else:
            self.draw_border = False

    async def loop(self):
        self.handle_focus()
        await super().loop()


class ItemList(Interface):
    items: str = None  # Pointer to a list matching the item schema.
    scroll: float = None
    margin: float = None
    item_size: tuple[int, int] = None

    draw_rect = True
    draw_border = True

    def build_items(self):
        for index, item in enumerate(self[self.items]):
            item_name = f'item_{index}'
            self.add_child(
                Item(
                    item_name,
                    title=item.get('title'),
                    body=item.get('body'),
                    position=(
                        self.rect.left + self.margin,
                        self.rect.top + self.margin + (self.item_size[1] + self.margin) * index
                    ),
                    size=self.item_size,
                )
            )

    def build(self):
        self(
            self.name,
            Trigger(
                'on_items_change_trigger',
                value='../items'
            ),
            Trigger(
                'on_scroll_trigger',
                value='../scroll'
            ),
            Interface(
                'scroll_bar',
                size=(10, 0),
                draw_rect=True,
                draw_border=False,
                fill_color=(100, 100, 100),
            ),
        )
        super().build()

    def place_scroll_bar(self):
        ...

    def fit(self):
        self.initattr('item_size', (200, 20))
        self.initattr('margin', 4.0)
        self.initattr('items', [])
        self.initattr('scroll', 0.0)
        super().fit()
        self.build_items()

    def handle_scroll(self):
        ...

    def handle_items_change(self):
        if self.on_items_change_trigger.handle():
            self.build_items()

    async def loop(self):
        self.handle_items_change()
        await super().loop()
