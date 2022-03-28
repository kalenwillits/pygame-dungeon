from core.node import Node

from components.text import Text
# from components.trigger import Trigger

RELATIVE_POINTER = '../camera/collision_layer/map/player/stats/'


class HeadsUpDisplay(Node):
    def build(self):
        self(
            self.name,
            Text(
                'name',
                text_size='xs',
                anchor='topleft'
            ),
            Text(
                'health',
                text_size='xs',
                anchor='topleft',
                position=(0, self['/style/text/xs_character_size'][1])
            ),
        )
        super().build()

    def sync_health(self):
        health_value = 'HP: ' + str(
            self[f'{RELATIVE_POINTER}health']) + '/' + str(self[f'{RELATIVE_POINTER}max_health'])

        if health_value != self.health.value:
            self.health.set_value(health_value)

    def fit(self):
        super().fit()
        self.name.value = self['/cache']['character']['name']
        self.sync_health()

    async def loop(self):
        self.sync_health()
        await super().loop()
