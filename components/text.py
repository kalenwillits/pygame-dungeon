from pygame import Color
from core.interface import Interface
from components.trigger import Trigger


class Text(Interface):
    value: str = None
    text_size: str = None
    text_color: Color = None
    draw_rect = False
    draw_border = False
    margin: float = None

    def build(self):
        self.initattr('text_color', self.get_root().style.color.text)
        self.initattr('text_size', self.get_root().settings.text.text_size)
        self.initattr('value', '')
        self.rebuild()
        self(
            self.name,
            Trigger(
                'value_change_trigger',
                value='../value',
            )
        )
        super().build()

    def fit(self):
        self.initattr('margin', self.get_root().style.text.margin)
        super().fit()
        self.rebuild()

    def set_value(self, new_value):
        self.value = new_value

    def rebuild(self):
        self.build_sprite()
        self.build_rect()

    def build_sprite(self):
        self.sprite = self.get_root().style.text[f'{self.text_size}'].render(
            self.value,
            True,
            self.text_color
        )

    def build_rect(self):
        self.rect = self.sprite.get_rect(**self.get_rect_params())

    def handle_value_change(self):
        if self.value_change_trigger.handle():
            self.rebuild()

    async def loop(self):
        self.handle_value_change()
        await super().loop()
