from engine.app import App
from core.node import Node
from config.settings import Settings
from config.keybinds import Keybinds
from config.style import Style
from engine.cursor import Cursor
from engine.events import Events
from engine.tasks import Tasks
from core.resource import Resource
from components.data import Data

from views.start.view import Start
from views.game.view import Game
from views.character.create import CharacterCreate
from views.character.overview import CharacterOverview


app = App(
    'app',
    Settings('settings'),
    Data('data'),
    Style('style'),
    Cursor('cursor'),
    Keybinds('keybinds'),
    # --------------------------------------------------------------------------------------------------------------- #
    Node(
        'resources',
        Resource(
            'spritesheet',
            source='resources/spritesheet.png',
        ),
    ),
    Node(
        'menu',
        Start('start'),
        CharacterCreate('character_create'),
        CharacterOverview('character_overview'),
    ),
    Node(
        'main',
        Game('game'),
    ),
    # --------------------------------------------------------------------------------------------------------------- #
    Events('events'),
    Tasks('tasks'),
)


if __name__ == '__main__':
    app.run()
