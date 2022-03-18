from pygame import Color
from pygame import mouse

from core.interface import Interface
from .timer import Timer


class Button(Interface):
    is_toggle: bool = False

    enable_idle: bool = True
    enable_hover: bool = True
    enable_pressed: bool = True
    enable_disabled: bool = True

    state: str = 'idle'
    previous_state: str = None
    colors: dict[str, Color] = {}
    cooldown: int = None
    cursor_in: bool = False
    previous_cursor_in: bool = False

    on_cursor_enter: callable = None
    on_cursor_exit: callable = None
    on_press: callable = None
    on_release: callable = None

    def build(self):
        self(
            self.name,
            Timer(
                'timer'
            )
        )
        super().build()

    def fit(self):
        self.initattr('cooldown', self.get_root().settings.button.cooldown)
        self.colors['idle'] = self.get_root().style.color.idle
        self.colors['hover'] = self.get_root().style.color.hover
        self.colors['pressed'] = self.get_root().style.color.pressed
        self.colors['disabled'] = self.get_root().style.color.disabled
        super().fit()
        self.timer.start()

    def set_hover(self):
        if self.enable_hover:
            self.state = 'hover'

    def set_pressed(self):
        if self.enable_pressed:
            self.state = 'pressed'

    def set_idle(self):
        if self.enable_idle:
            self.state = 'idle'

    def set_disabled(self):
        if self.enable_disabled:
            self.state = 'disabled'

    def get_state(self) -> str:
        return self.state

    def state_trigger(self) -> bool:
        if self.state != self.previous_state:
            self.previous_state = self.state
            return True
        return False

    def cursor_trigger(self) -> bool:
        if self.cursor_in != self.previous_cursor_in:
            self.previous_cursor_in = self.cursor_in
            return True
        return False

    def handle_cursor_enter(self):
        self.cursor_in = True
        if self.cursor_trigger() and self.on_cursor_enter is not None:
            self.on_cursor_enter(self)

    def handle_cursor_exit(self):
        self.cursor_in = False
        if self.cursor_trigger() and self.on_cursor_exit is not None:
            self.on_cursor_exit(self)

    def handle_color(self):
        self.fill_color = self.colors[self.get_state()]

    def handle_toggle_state(self):
        if self.rect.collidepoint(self.get_root().cursor.position):
            self.handle_cursor_enter()

            if mouse.get_pressed()[0] and self.timer.timestamp > self.cooldown:
                if self.get_state() == 'idle':
                    self.set_pressed()
                    if self.on_press is not None:
                        self.on_press(self)
                else:
                    self.set_idle()
                    if self.on_release is not None:
                        self.on_release(self)
                self.timer.start()
        else:
            self.handle_cursor_exit()

    def handle_standard_state(self):
        if self.rect.collidepoint(self.get_root().cursor.position):
            self.handle_cursor_enter()

            if mouse.get_pressed()[0]:
                self.set_pressed()
                if self.on_press is not None:
                    self.on_press(self)
                self.timer.start()
            else:
                if self.state_trigger():
                    if self.previous_state == 'pressed':
                        if self.on_release is not None:
                            self.on_release(self)
                self.set_hover()

        else:
            self.set_idle()
            self.handle_cursor_exit()

    def handle_state(self):
        if not self.get_state() == 'disabled':
            getattr(self, f'handle_{"toggle" if self.is_toggle else "standard"}_state')()

    async def loop(self):
        self.handle_state()
        await super().loop()

    async def draw(self):
        self.handle_color()
        await super().draw()
