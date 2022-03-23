from collections import defaultdict
import pygame

from core.node import Node


TYPE_SIGNAL_MAP = {
    pygame.KEYDOWN: 'on_key_down',
    pygame.KEYUP: 'on_key_up',
    pygame.MOUSEWHEEL: 'on_mouse_wheel',
    pygame.MOUSEBUTTONUP: 'on_mouse_button_up',
    pygame.MOUSEBUTTONDOWN: 'on_mouse_button_down',
}

SIGNAL_TYPE_MAP = {signal: type for type, signal in TYPE_SIGNAL_MAP.items()}


class Events(Node):
    on_key_down: dict[str, str] = defaultdict(lambda: None, {})
    on_key_pressed: dict[str, str] = defaultdict(lambda: None, {})
    on_key_up: dict[str, str] = defaultdict(lambda: None, {})
    on_mouse_button_down: dict[str, str] = defaultdict(lambda: None, {})
    on_mouse_button_pressed: dict[str, str] = defaultdict(lambda: None, {})
    on_mouse_button_up: dict[str, str] = defaultdict(lambda: None, {})
    on_mouse_wheel: dict[str, str] = defaultdict(lambda: None, {})

    generic_event_queue: set[str] = set()

    def connect(self, event_type: str, keybind: str, signal: str):
        self[event_type].update({keybind: signal})

    def disconnect(self, event_type: str, keybind: str):
        self[event_type][keybind] = None

    def add_event_handler(self, event_handler):
        self.generic_event_queue.add(event_handler)

    def remove_event_handler(self, event_handler_path: str):
        if event_handler_path in self.generic_event_queue:
            self.generic_event_queue.remove(event_handler_path)

    def get_signal_event_state(self, signal_name, event):
        if event.key == self.get_root().keybinds[TYPE_SIGNAL_MAP[event.type]][signal_name]:
            return True
        return False

    def state_change_signal_handler(self, event):
        if valid_signal := TYPE_SIGNAL_MAP.get(event.type):
            for signal_name, signal_path in self[valid_signal].items():
                if self.get_signal_event_state(signal_name, event):
                    if signal_path:
                        self.get_root()[signal_path]()
                        break

    def handle_events(self):
        # State change events
        for event in pygame.event.get():
            for event_handler_path in self.generic_event_queue:
                self.get_root()[event_handler_path](event)

            self.state_change_signal_handler(event)

            # Hard-coded quit event
            if event.type == pygame.QUIT:
                self.get_root().quit = True

        # Continuous key press events
        for signal_name, keys in self.get_root().keybinds.on_key_pressed.items():
            if all([pygame.key.get_pressed()[key] for key in keys]):
                if signal_func := self.get_root()[self.on_key_pressed[signal_name]]:
                    signal_func()

        # Continuous mouse press events
        for signal_name, buttons in self.get_root().keybinds.on_mouse_button_pressed.items():
            if all([pygame.mouse.get_pressed()[button] for button in buttons]):
                self.get_root()[self.on_mouse_button_pressed[signal_name]]()

    async def loop(self):
        self.handle_events()
