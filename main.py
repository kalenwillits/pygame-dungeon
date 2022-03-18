from engine.app import App
from core.node import Node
from config.settings import settings
from config.keybinds import Keybinds
from config.style import style
from engine.cursor import cursor
from engine.events import events
from engine.tasks import tasks

from start.start import start_view


app = App(
    'app',
    settings,
    style,
    cursor,
    Keybinds('keybinds'),

    Node(
        'menu',
        start_view,
    ),

    events,
    tasks,
)


if __name__ == '__main__':
    app.run()
