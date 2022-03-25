from core.node import Node


class CharacterCreate(Node):
    def build(self):
        self(
            self.name,
        )
        super().build()

    def fit(self):
        super().fit()

    async def loop(self):
        await super().loop()

    async def draw(self):
        await super().draw()
