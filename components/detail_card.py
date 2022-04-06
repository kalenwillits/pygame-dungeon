from pygame.math import Vector2 as Vector

from core.interface import Interface
from components.text import Text
from components.paragraph import Paragraph
from components.trigger import Trigger


class DetailCard(Interface):
    title: str = None
    body: str = None
    margin: float = 1

    card_size: tuple[float, float] = None

    draw_border = False
    draw_rect = False

    @property
    def is_hover(self) -> bool:
        if (hover_point := self['/cursor/hover']):
            return self.rect.collidepoint(hover_point)
        return False

    def build(self):
        self.initattr('card_size', (0, 0))
        self(
            self.name,
            Trigger(
                'card_trigger',
                value='../is_hover'
            ),
            Interface(
                'card',
                Text(
                    'title_text',
                    anchor='top',
                    text_size='xs',
                    value=self.title,
                ),
                Paragraph(
                    'body_paragraph',
                    value=self.body,
                    anchor='top',
                    text_size='xs',
                    size=(self.card_size[0] - self.margin, self.card_size[1] - self.margin),
                    ),
                size=self.card_size,
                anchor=self.anchor,
                grid=self.grid,
                cols=self.cols,
                col=self.col,
                rows=self.rows,
                row=self.row,
                border_color=self.border_color,
                draw_rect=True,
                draw_border=True,
            ),
        )
        super().build()

    def fit(self):
        super().fit()
        self.hide_card()
        self.place_content()

    def place_content(self):
        self.card.title_text.position = Vector(self.card.rect.centerx, self.card.rect.top + self.margin)
        self.card.body_paragraph.position = Vector(
            self.card.rect.centerx,
            self.card.rect.top + (self.margin * 2) + self['/style/text/xs_character_size'][1]
        )

    def hide_card(self):
        self.set_view(['card_trigger'])

    def show_card(self):
        self.set_view(['card', 'card_trigger'])

    def handle_card_state(self):
        if self.card_trigger.handle():
            if self.is_hover:
                self.show_card()
            else:
                self.hide_card()

    async def loop(self):
        self.handle_card_state()
        await super().loop()
