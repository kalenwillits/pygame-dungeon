import pymunk
from core.node import Node
from core.body import Body


class Space(Node):
    damping: float = None
    gravity: float = None

    def __init__(self, name: str, *nodes, **kwargs):
        self.space = pymunk.Space()
        super().__init__(name, *nodes, **kwargs)

    @property
    def gravity(self) -> tuple[float, float]:
        return self.space.gravity

    @gravity.setter
    def gravity(self, value: tuple[float, float]):
        self.space.gravity = value

    @property
    def damping(self) -> float:
        return self.space.damping

    @damping.setter
    def damping(self, value: float):
        self.space.damping = value

    def add_collision_handler(self, body, layer: int):
        if isinstance(body, str):
            body = self.get_root()[body]

        collision_handler = self.space.add_collision_handler(body.layer, layer)
        collision_handler.begin = body.on_collision
        collision_handler.pre_solve = body.pre_solve
        collision_handler.post_solve = body.post_solve
        collision_handler.separate = body.on_seperate

    def startup(self):
        self.damping = self.kwargs.get('damping', self.get_root().settings.physics.damping)
        self.gravity = self.kwargs.get('gravity', self.get_root().settings.physics.gravity)

    def fit(self):
        super().fit()
        self.cascade(f'{self.get_path()}/add_body')

    def add_body(self, body: Body):
        if isinstance(body, Body):
            self.space.add(body.body, body.shape)

    def remove_body(self, body_node):
        self.space.remove(body_node.body, body_node.shape)

    async def loop(self):
        await super().loop()
        self.space.step(self.get_root().delta)
