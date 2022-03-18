import pygame

from .text import Text
from .button import Button

# TODO - Add Truncate when not active and overflowing
# - Overflow should be able to scroll backwards and forwards
# - The cursor goes off the component when overflowing.


class Input(Button):
    cursor_position: int = 0

    enter_edit_mode: bool = False
    previous_enter_edit_mode: bool = None

    exit_edit_mode: bool = False
    previous_exit_edit_mode: bool = None
    initial_value: str = ''

    on_change: callable = lambda self: None
    previous_text_value: str = None

    max_characters: int = None
    value: str = ''

    def build(self):
        self(
            self.name,
            Text(
                'text',
                value=self.value,
                rect=self.rect,
                grid=True,
                cols=self.cols,
                col=self.col,
                rows=self.rows,
                row=self.row,
            ),
            Text(
                'cursor',
                value='_',
                cols=self.cols,
                col=self.col,
                rows=self.rows,
                row=self.row,
            )
        )
        super().build()
        # TODO set anchors to left

    def on_change_trigger(self) -> bool:
        if self.value != self.previous_text_value:
            self.previous_text_value = self.value
            return True
        return False

    def enter_edit_mode_trigger(self) -> bool:
        if self.enter_edit_mode != self.previous_enter_edit_mode:
            self.previous_enter_edit_mode = self.enter_edit_mode
            return True
        return False

    def exit_edit_mode_trigger(self) -> bool:
        if self.exit_edit_mode != self.previous_exit_edit_mode:
            self.previous_exit_edit_mode = self.exit_edit_mode
            return True
        return False

    def handle_view_state(self):
        if self.state == 'pressed':
            self.set_view({'text', 'timer', 'cursor'})
        else:
            self.set_view({'text', 'timer'})

    def handle_overflow(self):
        if (self.cursor.size[0] * self.cursor_position) > (self.size[0] - self.text.margin * 2):
            cutoff = len(self.value) - int((self.size[0] - (self.text.margin * 2)) / self.cursor.size[0])
            self.text.value = self.value[cutoff:]
        else:
            self.text.value = self.value

    def handle_on_change(self):
        if self.on_change_trigger():
            self.handle_overflow()
            self.on_change(self)

    def handle_input_event(self, event):
        if self.get_state() == 'pressed':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    self.exit_edit_mode = not self.exit_edit_mode
                    self.set_idle()
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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.rect.collidepoint(self.get_root().cursor.position):
                    self.exit_edit_mode = not self.exit_edit_mode
                    self.set_idle()

    def fit(self):
        self.text.set_value(self.initial_value)

        def handle_press(self):
            self.enter_edit_mode = not self.enter_edit_mode

        def handle_release(self):
            self.exit_edit_mode = not self.exit_edit_mode

        self.on_press = handle_press
        self.on_release = handle_release

        super().fit()

    def handle_edit_mode(self):
        if self.enter_edit_mode_trigger():
            self.is_toggle = True
            self.get_root().events.add_event_handler(f'{self.get_path()}/handle_input_event')

        if self.exit_edit_mode_trigger():
            self.is_toggle = False
            self.get_root().events.remove_event_handler(f'{self.get_path()}/handle_input_event')

    def handle_cursor_position(self):
        self.cursor.position = (
            self.text.position[0] + (self.cursor.size[0] / 2) * self.cursor_position,
            self.text.position[1]
        )

    async def loop(self):
        await super().loop()
        self.handle_view_state,
        self.handle_edit_mode,
        self.handle_cursor_position,
        self.handle_on_change,

