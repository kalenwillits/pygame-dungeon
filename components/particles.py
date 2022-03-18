from collections import defaultdict
from random import randint, choice

from core.object import Object
from pygame import Color
from pygame.math import Vector2 as Vector
import pygame


SHAPES = defaultdict(lambda: 'polygon', {
    1: 'circle',
    2: 'line',
    3: 'polygon',
})


class Particle:
    def __init__(
        self,
        position: Vector = Vector(),
        vertices: list[tuple[int, int], ...] = [(0, 0)],
        color: Color = Color(255, 255, 255),
        lifespan: int = 10,
        radius: int = 10,
    ):
        self.lifetime = 0
        self.vertices = vertices
        self.lifespan = lifespan
        self.color = color
        self.radius = radius

    @property
    def shape(self) -> str:
        return SHAPES[len(self.vertices)]

    @property
    def position(self) -> Vector:
        return self.vertices[0]

    @position.setter
    def position(self, value: tuple[float, float]):
        self.vertices = [(vertex[0] + value[0], vertex[1] + value[1]) for vertex in self.vertices]

    @property
    def params(self):
        if self.shape == 'circle':
            return [self.position, self.radius]
        elif self.shape == 'line':
            return self.vertices
        else:
            return [self.vertices]

    def is_alive(self) -> bool:
        return self.lifetime < self.lifespan


class Particles(Object):
    quantity: tuple[int, int] = None
    delay: tuple[int, int] = None
    repeat: int = None
    scale: float = None
    behavior: callable = None
    velocity: tuple[int, int] = None
    colors: list[Color, ...] = None
    vertices: list[list[tuple[int, int], tuple[int, int]], ...] = None
    radius: tuple[float, float] = None
    lifespan: tuple[int, int] = None

    frame: int = None
    queue: list[Particle] = None
    is_playing: bool = False
    is_paused: bool = False

    def build(self):
        super().build()

    def behavior(self, particle):
        particle.position[0] += randint(*self.velocity[0])*self.get_root().delta
        particle.position[1] += randint(*self.velocity[1])*self.get_root().delta
        particle.radius -= self.get_root().delta*0.1

    def fit(self):
        self.initattr('quantity', self.get_root().settings.particles.quantity)
        self.initattr('scale', self.get_root().settings.particles.scale)
        self.initattr('repeat', self.get_root().settings.particles.repeat)
        self.initattr('velocity', self.get_root().settings.particles.velocity)
        self.initattr('colors', self.get_root().settings.particles.colors)
        self.initattr('vertices', self.get_root().settings.particles.vertices)
        self.initattr('delay', self.get_root().settings.particles.delay)
        self.initattr('radius', self.get_root().settings.particles.radius)
        self.initattr('lifespan', self.get_root().settings.particles.lifespan)

        self.initattr('frame', 0)
        self.initattr('queue', [])
        super().fit()

    def generate(self):
        for _ in range(randint(*(self.quantity*self.scale))):
            self.queue.append(
                Particle(
                    position=self.position,
                    vertices=self.generate_verticies(),
                    color=self.generate_color(),
                    lifespan=self.generate_lifespan(),
                    radius=self.generate_radius(),
                )
            )

    def generate_verticies(self):
        return [
            Vector(
                self.position[0] + randint(*vertex[0]),
                self.position[1] + randint(*vertex[1])
            ) for vertex in self.vertices]

    def generate_color(self):
        return choice(self.colors)

    def generate_lifespan(self):
        return randint(*self.lifespan)

    def generate_radius(self):
        return randint(*self.radius)

    def play(self):
        self.is_playing = True

    def pause(self):
        self.is_paused = True

    def unpause(self):
        self.is_paused = False

    def stop(self):
        self.is_playing = False
        self.is_paused = False
        self.frame = 0

    def handle_behavior(self):
        if self.is_playing and not self.is_paused:
            if self.frame == 0:
                self.generate()
            self.frame += self.get_root().delta
            self.queue = list(filter(lambda particle: particle.is_alive(), self.queue))
            for particle in self.queue:
                self.behavior(particle)
                particle.lifetime += self.get_root().delta

            if self.frame > randint(*self.delay):
                self.generate()

            if self.repeat > 0:
                if (self.frame / (sum(self.delay) / 2)) > self.repeat:
                    self.stop()

    async def loop(self):
        self.handle_behavior()
        await super().loop()

    def render(self):
        if self.is_playing:
            for particle in self.queue:
                getattr(pygame.draw, particle.shape)(
                    self.get_root().display,
                    particle.color,
                    *particle.params,
                )

    async def draw(self):
        self.render()
        await super().draw()



