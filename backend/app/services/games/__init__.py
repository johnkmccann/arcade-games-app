"""
Game implementations using the GameAdapter pattern.

Each game is self-contained in its own module and can be developed/tested independently.
Games can be added by creating a new subdirectory with an adapter.py file.
"""

from app.services.game_adapter import GameRegistry
from .chess import ChessAdapter
from .tetris import TetrisAdapter
from .pacman import PacManAdapter
from .darts import DartsAdapter


# Game registry initialization
def register_default_games():
    """Register the default games that come with the platform"""
    GameRegistry.register('chess', ChessAdapter())
    GameRegistry.register('tetris', TetrisAdapter())
    GameRegistry.register('pacman', PacManAdapter())
    GameRegistry.register('darts', DartsAdapter())


__all__ = [
    'ChessAdapter',
    'TetrisAdapter',
    'PacManAdapter',
    'DartsAdapter',
    'register_default_games',
]
