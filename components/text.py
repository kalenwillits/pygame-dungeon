from pygame import Color
from core.interface import Interface
from core.trigger import Trigger


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
        self.build_sprite()
        self.build_rect()
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

    def set_value(self, new_value):
        self.value = new_value

    def build_sprite(self):
        self.sprite = self.get_root().style.text[f'{self.text_size}'].render(
            self.value,
            True,
            self.text_color
        )

    def build_rect(self):
        # TODO recheck this moving forward, since size comes from rect, we don't need this anymore
        # self.size = self.sprite.get_size()
        self.rect = self.sprite.get_rect(**self.get_rect_params())

    def handle_value_change(self):
        if self.value_change_trigger.handle():
            self.build_sprite()
            self.build_rect()

    async def loop(self):
        self.handle_value_change()
        await super().loop()
