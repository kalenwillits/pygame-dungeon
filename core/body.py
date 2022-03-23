from collections import defaultdict

import pymunk
from core.node import Node

from pygame.math import Vector2 as Vector


BODY_TYPES = {
        pymunk.Body.DYNAMIC: pymunk.Body.DYNAMIC,
        pymunk.Body.KINEMATIC: pymunk.Body.KINEMATIC,
        pymunk.Body.STATIC: pymunk.Body.STATIC,
        'dynamic': pymunk.Body.DYNAMIC,
        'kinematic': pymunk.Body.KINEMATIC,
        'static': pymunk.Body.STATIC,
    }


BODY_SHAPES = defaultdict(
    lambda: pymunk.Poly, {
        0: pymunk.Circle,
        1: pymunk.Circle,
        2: pymunk.Segment,
    }
)


class Body(Node):
    body: pymunk.Body = None
    shape: pymunk.Shape = None
    is_sensor: bool = False
    moment: float = None
    density: float = None
    radius: float = None
    sync_rotation: bool = True
    _acceleration: float = None
    max_velocity: float = None
    _attr_cache: dict = None

    def __init__(self, name, *nodes, **kwargs):
        self._attr_cache = {}
        super().__init__(name, *nodes, **kwargs)

    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value: float):
        self._acceleration = value

    @property
    def angle(self) -> float:
        return self.body.angle

    @angle.setter
    def angle(self, value: float):
        if self.body is None:
            self._attr_cache['angle'] = value
        else:
            self.body.angle = value

    @property
    def density(self) -> float:
        return self.shape.density

    @density.setter
    def density(self, value: float):
        if self.shape is None:
            self._attr_cache['density'] = value
        else:
            self.shape.density = value

    @property
    def mass(self) -> float:
        return self.body.mass

    @mass.setter
    def mass(self, value: float):
        if self.body is None:
            self._attr_cache['mass'] = value
        else:
            self.body.mass = value

    @property
    def damping(self) -> float:
        return self.shape.damping

    @damping.setter
    def damping(self, value: float):
        if self.shape is None:
            self._attr_cache['damping'] = value
        else:
            self.shape.damping = value

    @property
    def friction(self) -> float:
        return self.shape.friction

    @friction.setter
    def friction(self, value: float):
        if self.shape is None:
            self._attr_cache['friction'] = value
        else:
            self.shape.friction = value

    @property
    def moment(self) -> float:
        return self.shape.moment

    @moment.setter
    def moment(self, value: float):
        if self.shape is None:
            self._attr_cache['moment'] = value
        else:
            self.shape.moment = value

    @property
    def elasticity(self) -> float:
        return self.shape.elasticity

    @elasticity.setter
    def elasticity(self, value: float):
        if self.shape is None:
            self._attr_cache['elasticity'] = value
        else:
            self.shape.elasticity = value

    @property
    def torque(self) -> float:
        return self.shape.elasticity

    @torque.setter
    def torque(self, value: float):
        if self.body is None:
            self._attr_cache['torque'] = value
        else:
            self.body.torque = value


    @property
    def layer(self) -> int:
        return self.shape.collision_type

    @layer.setter
    def layer(self, value: int):
        if self.shape is None:
            self._attr_cache['layer'] = value
        else:
            self.shape.collision_type = value

    @property
    def velocity(self) -> float:
        return self.body.velocity

    @velocity.setter
    def velocity(self, value: tuple[float, float]):
        self.body.velocity = value

    def get_anchor_offset_from_body(self) -> Vector:
        '''
        Returns the offset for the body in relation to the rect size and anchor position.
        The pymunk body's origin is always in the center. When we choose an anchor, this will offset the vertices
        before the body is built to account for this difference.
        '''
        return {
            'center': Vector((0, 0)),
            'top': Vector(0, int(self.rect.size[1] / 2)),
            'topleft': Vector(int(self.rect.size[0] / 2), int(self.rect.size[0] / 2)),
            'left': Vector(int(self.rect.size[0] / 2), 0),
            'bottomleft': Vector(int(self.rect.size[0] / 2), -int(self.rect.size[1] / 2)),
            'bottom': Vector(0, -int(self.rect.size[1] / 2)),
            'bottomright': Vector(-int(self.rect.size[0] / 2), -int(self.rect.size[1] / 2)),
            'right': Vector(-int(self.rect.size[0] / 2), 0),
            'topright': Vector(-int(self.rect.size[0] / 2), int(self.rect.size[1] / 2)),
        }[self.anchor]

    def fit_vertices_with_offset(self):
        offset = self.get_anchor_offset_from_body()
        self.vertices = [
          [x + offset[0], y + offset[1]] for x, y in self.vertices
        ]

    # def handle_max_velocity(self):
    #     if self.velocity.length > self.max_velocity:
    #         self.velocity = self.velocity.normalized() * self.max_velocity

    def impulse(self, force: tuple, point=None, mode: str = 'world', type='impulse'):
        getattr(self.body, f'apply_{type}_at_{mode}_point')(force, self.body.position if point is None else point)

    def on_collision(self, arbiter, space, data) -> bool:
        '''
        Two shapes just started touching for the first time this step.
        '''
        return True

    def pre_solve(self, arbiter, space, data) -> bool:
        '''
        Two shapes are touching during this step.
        '''
        return True

    def post_solve(self, arbiter, space, data) -> bool:
        '''
        Two shapes are touching and their collision response has been processed.
        '''
        return True

    def on_seperate(self, arbiter, space, data) -> bool:
        '''
        Two shapes have just stopped touching for the first time this step.
        '''
        return True

    def compile_body_and_shape(self):
        self.body = pymunk.Body(body_type=BODY_TYPES[(self.body_type)])
        self.body.position = self.position.x, self.position.y
        self.body.velocity_func = self.limit_velocity
        self.shape = BODY_SHAPES[len(self.vertices)](
            self.body,
            self.vertices if len(self.vertices) > 1 else 10.0,
            )
        self.shape.sensor = self.is_sensor

        if self._attr_cache:
            for attr, value in self._attr_cache.items():
                setattr(self, attr, value)
            delattr(self, '_attr_cache')

    def add_mask(self, mask: str):
        self.masks.append(mask)

    def remove_mask(self, mask: str):
        self.masks.remove(mask)

    def limit_velocity(self, body, gravity, damping, dt):
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        length = body.velocity.length
        if length > self.max_velocity:
            scale = self.max_velocity / length
            body.velocity = body.velocity * scale

    def fit(self):
        self.initattr('vertices', [])
        self.fit_vertices_with_offset()
        self.initattr('acceleration', self.get_root().settings.physics.acceleration)
        self.initattr('max_velocity', self.get_root().settings.physics.max_velocity)
        self.initattr('elasticity', self.get_root().settings.physics.elasticity)
        self.initattr('friction', self.get_root().settings.physics.friction)
        self.initattr('body_type', self.get_root().settings.physics.body_type)
        if pymunk.Body.KINEMATIC != BODY_TYPES[self.body_type] != pymunk.Body.STATIC:
            self.initattr('mass', self.get_root().settings.physics.mass)
            self.initattr('density', self.get_root().settings.physics.density)
            self.initattr('torque', self['/settings/physics/torque'])

        self.compile_body_and_shape()
        super().fit()

    async def loop(self):
        # self.handle_max_velocity()
        await super().loop()
