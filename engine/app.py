import asyncio
import traceback
import sys
import time

from pygame import quit
from pygame import Surface
from pygame.time import Clock
from pygame import mixer
from pygame.transform import scale
import pygame

from core.node import Node


class App(Node):
    quit: bool = False
    display: Surface = None
    clock = Clock()
    delta: float = 0.0
    starttime = None
    endtime = None
    mixer = mixer
    init_queue: list[str] = ['settings', 'style', '.']

    def get_framerate(self) -> int:
        return self.clock.get_fps()

    def render(
        self,
        node: Node,
        fill_color: tuple[int, int, int] = None,
        border_color: tuple[int, int, int] = None,
        border_radius: int = None,
        border_width: int = None,
        outline_color: tuple[int, int, int] = None,
    ):
        offset_rect = node.rect.move(-node.offset)
        if self.display_rect.colliderect(offset_rect):
            if fill_color is None:
                fill_color = self.style.color.idle
            if border_radius is None:
                border_radius = self.style.rect.border_radius
            if border_width is None:
                border_width = self.style.rect.border_width
            if outline_color is None:
                outline_color = self.style.color.outline

            if node.draw_rect:
                # Draw the fill rect
                pygame.draw.rect(
                    self.display,
                    fill_color,
                    offset_rect,
                    border_radius=border_radius
                    )
            # Draw the rect border
            if node.draw_border:
                pygame.draw.rect(
                    self.display,
                    self.style.color.border,
                    offset_rect,
                    width=border_width,
                    border_radius=border_radius,
                    )

            # TODO
            # Figure out the outline offset
            # Allow the outline to cycle through animations

            if node.draw_outline:
                self.display.blit(
                    node.outline,
                    node.get_sprite_offset() - node.offset,
                    area=node.area.move((0, -node.outline_width)),
                    special_flags=pygame.BLEND_ALPHA_SDL2
                )
                self.display.blit(
                    node.outline,
                    node.get_sprite_offset() - node.offset,
                    area=node.area.move((0, node.outline_width)),
                    special_flags=pygame.BLEND_ALPHA_SDL2
                )
                self.display.blit(
                    node.outline,
                    node.get_sprite_offset() - node.offset,
                    area=node.area.move((node.outline_width, 0)),
                    special_flags=pygame.BLEND_ALPHA_SDL2
                )
                self.display.blit(
                    node.outline,
                    node.get_sprite_offset() - node.offset,
                    area=node.area.move((-node.outline_width, 0)),
                    special_flags=pygame.BLEND_ALPHA_SDL2
                )

            if node.sprite and node.draw_sprite:
                self.display.blit(
                    node.sprite,
                    node.get_sprite_offset() - node.offset,
                    area=node.area,
                    special_flags=pygame.BLEND_ALPHA_SDL2
                )

    def init(self):
        self.mixer.init(
            frequency=self.settings.mixer.frequency,
            size=self.settings.mixer.size,
            buffer=self.settings.mixer.buffer,
        )

        pygame.init()
        self.window = pygame.display.set_mode(
            self.settings.user.resolution, pygame.FULLSCREEN if self.settings.full_screen else pygame.NOFRAME)
        pygame.display.set_caption(self.settings.window_caption)

        if self.settings.window_icon_source:
            pygame.display.set_icon(self.settings.window_icon_source)

        self.display = Surface(self.settings.resolution)
        self.display_rect = self.display.get_rect()

        super().init()

    async def draw(self):
        frame = scale(self.display, self.settings.user.resolution)
        self.window.blit(frame, frame.get_rect())
        self.display.fill(self.style.color.background)
        pygame.display.flip()
        await super().draw()

    async def main_loop(self):

        for node_path in self.init_queue:
            self[node_path].init()

        try:
            self.startup()
            self._status += 1
            self.build()
            self._status += 1
            self.fit()
            self._status += 1

            self.endtime = time.time()
            while True:
                self.starttime = time.time()
                self.delta = (self.starttime - self.endtime) * self.get_framerate()
                self.endtime = self.starttime

                self.clock.tick(self.settings.max_framerate)
                self.tasks.add(self.loop())
                self.tasks.add(self.draw())

                await self.tasks.run()

                if self.quit:
                    break

        except Exception:
            if self.settings.debug:
                traceback.print_exc()

        finally:
            for task in self.tasks.queue:
                if not task.done():
                    task.cancel()

            self.shutdown()
            quit()
            sys.exit()

    def run(self):
        asyncio.run(self.main_loop())
