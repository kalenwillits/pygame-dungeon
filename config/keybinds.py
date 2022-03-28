import pygame

from core.node import Node

MULTI_SCHEMA = dict[str, tuple[int, ...]]
SINGLE_SCHEMA = dict[str, int]

KEYBIND_TYPES = ('on_key_down', 'on_key_pressed', 'on_key_up', 'on_mouse_button_down', 'on_mouse_button_up',
                 'on_mouse_button_pressed')


class Keybinds(Node):
    on_key_down: SINGLE_SCHEMA = {
        'enter': pygame.K_RETURN,
        'camera_lock': pygame.K_SPACE,
    }
    on_key_pressed: MULTI_SCHEMA = {
        'move_up': [pygame.K_w],
        'move_left': [pygame.K_a],
        'move_right': [pygame.K_d],
        'move_down': [pygame.K_s],
        'look_up': [pygame.K_UP],
        'look_left': [pygame.K_LEFT],
        'look_right': [pygame.K_RIGHT],
        'look_down': [pygame.K_DOWN],
        'look_center': [pygame.K_SPACE],
        'look_up_left': [pygame.K_UP, pygame.K_LEFT],
        'look_up_right': [pygame.K_UP, pygame.K_RIGHT],
        'look_down_left': [pygame.K_DOWN, pygame.K_LEFT],
        'look_down_right': [pygame.K_DOWN, pygame.K_RIGHT],
    }
    on_key_up: SINGLE_SCHEMA = {
        'toggle_menu': pygame.K_ESCAPE,
    }
    on_mouse_button_down: SINGLE_SCHEMA = {
        'left_click': 0,
    }
    on_mouse_button_pressed: MULTI_SCHEMA = {

    }
    on_mouse_button_up: SINGLE_SCHEMA = {

    }

    def bind(self, event_type: str, keybind_name: str, keybind_value):
        assert event_type in KEYBIND_TYPES, f'Not a valid event type "{event_type}". Options are {KEYBIND_TYPES}'
        self[event_type][keybind_name] = keybind_value

    def unbind(self, event_type: str, keybind_name: str):
        del self[event_type][keybind_name]
