from engine.app import App
from core.node import Node
from config.settings import settings
from config.keybinds import Keybinds
from config.style import style
from engine.cursor import cursor
from engine.events import events
from engine.tasks import tasks

from views.start.view import start
from views.character_select.view import character_select

from components.data import Data


app = App(
    'app',
    settings,
    Data('data'),
    style,
    cursor,
    Keybinds('keybinds'),

    Node(
        'menu',
        start,
        character_select,
    ),

    events,
    tasks,
)


if __name__ == '__main__':
    app.run()
