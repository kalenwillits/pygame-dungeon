from engine.app import App
from core.node import Node
from config.settings import settings
from config.keybinds import Keybinds
from config.style import style
from engine.cursor import cursor
from engine.events import events
from engine.tasks import tasks
from core.resource import Resource

from views.start.view import start

from components.data import Data

from views.game.view import game


app = App(
    'app',
    settings,
    Data('data'),
    style,
    cursor,
    Keybinds('keybinds'),
    Resource(
        'spritesheet',
        source='resources/spritesheet.png',
    ),
    Node(
        'menu',
        start,
    ),
    Node(
        'main',
        game,
    ),
    events,
    tasks,
)


if __name__ == '__main__':
    app.run()
