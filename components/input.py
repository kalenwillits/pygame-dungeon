from core.interface import Interface
from core.trigger import Trigger
from components.text import Text
from components.timer import Timer

from pygame.math import Vector2 as Vector
from pygame import mouse
import pygame

VIEWS = {
    'idle': {'timer', 'state_trigger', 'text'},
    'edit': {'timer', 'state_trigger', 'value_trigger', 'text', 'cursor'},

}


class Input(Interface):
    cursor_position: int = 0
    state: str = None
    max_characters: int = None

    cooldown: int = None
    toggle_edit_mode: bool = False

    @property
    def value(self) -> str:
        return self.text.value

    @value.setter
    def value(self, value):
        self.text.value = value

    @property
    def text_size(self) -> str:
        return self.text.text_size

    @text_size.setter
    def text_size(self, value: str):
        self.text.text_size = value

    @property
    def text_size(self) -> str:
        return self.text.text_size

    @text_size.setter
    def text_size(self, value: str):
        self.text.text_size = value

    def build(self):
        self(
            self.name,
            Timer(
                'timer'
            ),
            Trigger(
                'value_trigger',
                value='../value'
            ),
            Trigger(
                'state_trigger',
                value='../state'
            ),
            Text(
                'text',
                rect=self.rect,
                grid=True,
                anchor='left',
            ),
            Text(
                'cursor',
                value='_',
                anchor='left',
            )
        )
        super().build()

    def place_text(self):
        position = Vector(self.rect.left + self.get_root().style.text.margin, self.rect.centery)
        self.text.position = position
        self.cursor.position = position

    def fit(self):
        self.initattr('value', self.kwargs.get('value', ''))
        self.initattr('cooldown', self.get_root().settings.input.cooldown)
        self.initattr('state', 'idle')
        super().fit()
        self.place_text()
        self.timer.start()
        self.set_view(VIEWS['idle'])

    def handle_state(self):
        if self.timer.timestamp > self.cooldown:
            if self.rect.collidepoint(self.get_root().cursor.position):
                if mouse.get_pressed()[0]:
                    self.state = 'edit'
                    self.enter_edit_mode()

            else:
                if mouse.get_pressed()[0]:
                    self.state = 'idle'
                    self.exit_edit_mode()
            self.timer.start()

    def enter_edit_mode(self):
        self.get_root().events.add_event_handler(f'{self.get_path()}/handle_input_event')

    def exit_edit_mode(self):
        self.get_root().events.remove_event_handler(f'{self.get_path()}/handle_input_event')

    def handle_cursor_position(self):
        self.cursor.position = (
            self.text.position[0] + self.cursor.size[0] * self.cursor_position,
            self.text.position[1]
        )

    def handle_input_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                self.toggle_edit_mode = not self.toggle_edit_mode
                self.state = 'idle'
            elif event.key == pygame.K_BACKSPACE:
                if len(self.value):
                    if self.cursor_position > 0:
                        self.value = f'{self.value[:self.cursor_position-1]}{self.value[self.cursor_position:]}'
                        if self.cursor_position > 0:
                            self.cursor_position -= 1
                        if event.mod & pygame.KMOD_CTRL:
                            self.value = ''
                            self.cursor_position = 0
            elif event.key == pygame.K_DELETE:
                self.value = f'{self.value[:self.cursor_position]}{self.value[self.cursor_position+1:]}'
            elif event.key == pygame.K_SPACE:
                self.value = f'{self.value[:self.cursor_position]}{" "}{self.value[self.cursor_position:]}'
                self.cursor_position += 1
            elif event.key == pygame.K_LEFT:
                self.cursor_position = max(self.cursor_position - 1, 0)
            elif event.key == pygame.K_RIGHT:
                self.cursor_position = min(self.cursor_position + 1, len(self.value))
            elif event.key == pygame.K_HOME:
                self.cursor_position = 0
            elif event.key == pygame.K_END:
                self.cursor_position = len(self.value)
            elif len(self.value) > (self.max_characters if self.max_characters else float('inf')):
                pass
            else:
                new_value = event.unicode.strip()
                self.value = f'{self.value[:self.cursor_position]}{new_value}{self.value[self.cursor_position:]}'
                self.cursor_position += len(new_value)

    def handle_view(self):
        if self.state_trigger.handle():
            self.set_view(VIEWS[self.state])

    def handle_overflow(self):
        if (self.cursor.size[0] * self.cursor_position) > (self.size[0] - self.text.margin * 2):
            cutoff = len(self.value) - int((self.size[0] - (self.text.margin * 2)) / self.cursor.size[0])
            self.value = self.value[cutoff:]
        else:
            self.value = self.value

    def handle_on_change(self):
        if self.value_trigger.handle():
            self.on_change(self)
            self.handle_overflow()

    async def loop(self):
        self.handle_state()
        self.handle_view()
        self.handle_cursor_position()
        await super().loop()
