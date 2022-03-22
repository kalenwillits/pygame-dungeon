from pygame.math import Vector2 as Vector
from core.node import Node


class Settings(Node):

    @property
    def scale_factor(self) -> float:
        return self.resolution[1] / self.user.resolution[1]


settings = Settings(
    'settings',
    Node( 'physics',
        gravity=(0.0, 0.0),
        density=1,
        mass=1,
        max_velocity=10,  # Max speed
        acceleration=2,  # How quickly you get to max speed
        damping=0.96,
        elasticity=1,
        friction=1,
        moment=1,
        body_type='dynamic',
    ),
    Node(
        'tilemap',
        tilesize=(16, 16)
    ),
    Node(
        'animation',
        framerate=20,
        radial='S',
        state='idle',
        radial_precision=1,
    ),
    Node(
        'mixer',
        frequency=44100,
        size=-16,
        buffer=512,
    ),
    Node(
        'user',
        resolution=Vector(int(1920/1.2), int(1080/1.2)),
    ),
    Node(
        'particles',
        repeat=-1,
        scale=1,
        colors=[(255, 255, 255)],
        velocity=[(-10, 10), (-10, 10)],
        vertices=[[(-1, 1), (-1, 1)]],
        quantity=(1, 10),
        delay=(1, 10),
        radius=(1, 10),
        lifespan=(10, 100)
    ),
    Node(
        'button',
        cooldown=20,
    ),
    Node(
        'input',
        cooldown=5
    ),
    Node(
        'text',
        text_size='sm',
    ),
    Node(
        'camera',
        smoothing=0.1,  # Speed of the camera's pan, too low and the camera can actually get left behind
        lookahead=64,  # Radius of the orbital around the target,
        tolerance=1,  # Snaps the the camera to the orbital when this close
    ),
    target_framerate=100,
    max_framerate=72,
    resolution=Vector(int(640), int(360)),
    full_screen=False,
    hide_cursor=False,
    debug=True,
    window_caption='Mythral Zero',
    window_icon_source=None,
)
