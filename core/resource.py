import os
from core.node import Node
from pygame import image


class Resource(Node):
    source: str = None
    content = None

    def build(self):
        assert self.source, f'{self.get_path()} is missing a source path.'
        self.content = image.load(os.path.join(self.source)).convert_alpha()
        super().build()
