from pygame.font import Font
import pygame
from pygame import Color
from core.node import Node


class Style(Node):
    def init(self):
        pygame.font.init()
        self(
            self.name,
            Node(
                'rect',
                border_radius=4,
                border_width=1,
                size=(
                    self.get_root().settings.resolution.x/3,
                    self.get_root().settings.resolution.y/35
                )
            ),
            Node(
                'color',
                text=Color(255, 255, 255),
                background=Color(20, 20, 20),
                idle=Color(45, 45, 45),
                pressed=Color(35, 35, 35),
                hover=Color(55, 55, 55),
                disabled=Color(25, 25, 25),
                border=Color(80, 80, 80),
                outline=Color(255, 255, 255),
                polygon=Color(255, 165, 0),
            ),
            Node(
                'text',
                source='resources/fonts/UbuntuMono-R.ttf',
                margin=int((self.get_root().settings.resolution.x / 200)),
                size_xs=int((self.get_root().settings.resolution.x / 80)),
                size_sm=int((self.get_root().settings.resolution.x / 60)),
                size_md=int((self.get_root().settings.resolution.x / 40)),
                size_lg=int((self.get_root().settings.resolution.x / 20)),
                size_xl=int((self.get_root().settings.resolution.x / 10)),


            ),
            Node(
                'outline',
                width=1,
            ),
            Node(
                'polygon',
                width=1,
            )
        )
        self.text.xs = Font(self.text.source, self.text.size_xs)
        self.text.xs_character_size = self.text.xs.render('_', True, (0, 0, 0)).get_size()
        self.text.sm = Font(self.text.source, self.text.size_sm)
        self.text.sm_character_size = self.text.sm.render('_', True, (0, 0, 0)).get_size()
        self.text.md: Font = Font(self.text.source, self.text.size_md)
        self.text.md_character_size = self.text.md.render('_', True, (0, 0, 0)).get_size()
        self.text.lg: Font = Font(self.text.source, self.text.size_lg)
        self.text.lg_character_size = self.text.lg.render('_', True, (0, 0, 0)).get_size()
        self.text.xl = Font(self.text.source, self.text.size_xl)
        self.text.xl_character_size = self.text.xl.render('_', True, (0, 0, 0)).get_size()
        super().init()
