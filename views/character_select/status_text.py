from components.text import Text
from core.trigger import Trigger


class StatusText(Text):
    def build(self):
        self(
            self.name,
            Trigger(
                'has_character_trigger',
                value='../character_is_created',
            ),
        )
        super().build()

    @property
    def character_is_created(self) -> bool:
        if self.get_root().data.get('character'):
            return True
        return False

    def fit(self):
        super().fit()

    def handle_value(self):
        if self.has_character_trigger.handle():
            self.value = '- Enter -'
        else:
            self.value = '- Create a character -'

    async def loop(self):
        self.handle_value()
        await super().loop()
