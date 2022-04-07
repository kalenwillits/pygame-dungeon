from core.interface import Interface
from components.detail_card import DetailCard
from components.text import Text
from components.trigger import Trigger

ITEM_SCHEMA = {
    'title': str,
    'body': str,
}


class Item(Interface):
    margin: float = None

    def build(self):
        self(
            self.name,
            Text(
                'item_name_text',
                value=self.kwargs.get('title'),
                anchor='left',
                text_size='xs',
            ),
            # TODO Format body from attributes
            DetailCard(
                'item_detail_card',
                title=self.kwargs.get('title'),
                body=self.kwargs.get('body'),
                card_size=(150, 150),
                card_anchor='topright',
                size=self.kwargs.get('size'),
                anchor='topleft',
                position=self.position,
                card_position=self.position
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


class ItemList(Interface):
    items: list[dict] = None
    scroll: float = None
    margin: float = None
    item_size: tuple[int, int] = None

    draw_rect = True
    draw_border = True

    def build_items(self):
        for index, item in enumerate(self.items):
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
            size=(300, 400),
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
