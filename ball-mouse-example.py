from math import sin, cos, pi, atan2
import pygame as pg

def get_angle(origin, destination):
    """Returns angle in radians from origin to destination.
    This is the angle that you would get if the points were
    on a cartesian grid. Arguments of (0,0), (1, -1)
    return .25pi(45 deg) rather than 1.75pi(315 deg).
    """
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    return atan2(-y_dist, x_dist) % (2 * pi)

def project(pos, angle, distance):
    """Returns tuple of pos projected distance at angle
    adjusted for pygame's y-axis.
    """
    return (pos[0] + (cos(angle) * distance),
            pos[1] - (sin(angle) * distance))


class HomingBullet(object):
    def __init__(self, pos, target_pos, speed=2.5):
        self.pos = pos
        self.angle = get_angle(self.pos, target_pos)
        self.speed = speed
        self.rect = pg.Rect(0, 0, 2, 2)
        self.rect.center = pos

    def update(self, target_pos):
        self.angle = get_angle(self.pos, target_pos)
        self.pos = project(self.pos, self.angle, self.speed)
        self.rect.center = self.pos

    def draw(self, surface):
        pg.draw.rect(surface, pg.Color("white"), self.rect)


class AngleTest(object):
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.screen = pg.display.set_mode((800, 800))
        self.done = False
        self.bullets = []

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.bullets.append(HomingBullet((400, 400), event.pos))

    def update(self):
        for bullet in self.bullets:
            bullet.update(pg.mouse.get_pos())

    def draw(self):
        self.screen.fill(pg.Color("black"))
        for bullet in self.bullets:
            bullet.draw(self.screen)

    def run(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    test = AngleTest()
    test.run()
    pg.quit()
