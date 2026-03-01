"""
Game Adapter Pattern - Scalable framework for adding new games

This module defines the abstract interface that all games must implement.
New games are added by creating a GameAdapter subclass without modifying
existing code, following the Open/Closed Principle.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from app.models.game import GameMetadata, GameSession


class GameAdapter(ABC):
    """
    Abstract base class for all game implementations.
    
    Each game type (Chess, Tetris, Pac-Man, etc.) should subclass this
    and implement the required methods.
    """
    
    @abstractmethod
    def get_metadata(self) -> GameMetadata:
        """Return metadata about this game type"""
        pass
    
    @abstractmethod
    def create_new_game(self, user_id: str, difficulty: Optional[str] = None) -> Dict[str, Any]:
        """
        Initialize a new game session's game_state.
        
        Args:
            user_id: The player starting the game
            difficulty: Optional difficulty level
            
        Returns:
            Initial game_state dict for this game
        """
        pass
    
    @abstractmethod
    def process_move(self, game_state: Dict[str, Any], move: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a player move and return updated game_state.
        
        Args:
            game_state: Current game state
            move: The move to process (format depends on game)
            
        Returns:
            Updated game_state
            
        Raises:
            ValueError: If move is invalid
        """
        pass
    
    @abstractmethod
    def is_game_over(self, game_state: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Determine if game is over and who won.
        
        Args:
            game_state: Current game state
            
        Returns:
            (is_over: bool, winner_user_id: Optional[str])
        """
        pass
    
    @abstractmethod
    def calculate_score(self, game_state: Dict[str, Any], duration_seconds: int) -> Dict[str, Any]:
        """
        Calculate score from final game state.
        
        Args:
            game_state: Final game state
            duration_seconds: How long game was played
            
        Returns:
            {
                'score_value': float,
                'score_breakdown': dict with scoring details
            }
        """
        pass
    
    @abstractmethod
    def validate_game_state(self, game_state: Dict[str, Any]) -> bool:
        """
        Validate that game_state is well-formed and legal.
        Useful for persistence recovery.
        """
        pass
    
    def get_legal_moves(self, game_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Optional: Return list of legal moves from current position.
        Useful for AI opponents and move validation.
        
        Returns empty list if not implemented.
        """
        return []
    
    def get_ai_move(self, game_state: Dict[str, Any], difficulty: str = "medium") -> Dict[str, Any]:
        """
        Optional: Return an AI move for single-player games.
        
        Args:
            game_state: Current game state
            difficulty: AI difficulty level
            
        Returns:
            Move dict in game's move format
            
        Raises:
            NotImplementedError: If game doesn't support AI
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not support AI opponents")


class GameRegistry:
    """
    Registry for all available games.
    
    Rather than hardcoding games, we maintain a registry.
    New games are registered without modifying existing code.
    """
    
    _games: Dict[str, GameAdapter] = {}
    
    @classmethod
    def register(cls, game_id: str, adapter: GameAdapter) -> None:
        """Register a new game adapter"""
        cls._games[game_id] = adapter
    
    @classmethod
    def unregister(cls, game_id: str) -> None:
        """Unregister a game adapter"""
        if game_id in cls._games:
            del cls._games[game_id]
    
    @classmethod
    def get(cls, game_id: str) -> Optional[GameAdapter]:
        """Get a game adapter by ID"""
        return cls._games.get(game_id)
    
    @classmethod
    def list_all(cls) -> List[GameMetadata]:
        """Get metadata for all registered games"""
        return [adapter.get_metadata() for adapter in cls._games.values()]
    
    @classmethod
    def is_registered(cls, game_id: str) -> bool:
        """Check if a game is registered"""
        return game_id in cls._games
    
    @classmethod
    def get_all_game_ids(cls) -> List[str]:
        """Get all registered game IDs"""
        return list(cls._games.keys())


# Example implementation templates
class SimpleArcadeGameAdapter(GameAdapter):
    """Base class for simple arcade games (Pac-Man, Space Invaders, etc.)"""
    
    def calculate_score(self, game_state: Dict[str, Any], duration_seconds: int) -> Dict[str, Any]:
        """
        Default arcade game scoring:
        - Base points from game state
        - Time bonus (more points for faster completion)
        """
        base_points = game_state.get('points', 0)
        time_bonus = max(0, (300 - duration_seconds) * 10) if duration_seconds < 300 else 0
        
        return {
            'score_value': base_points + time_bonus,
            'score_breakdown': {
                'base_points': base_points,
                'time_bonus': time_bonus,
                'duration_seconds': duration_seconds
            }
        }


class BoardGameAdapter(GameAdapter):
    """Base class for board games (Chess, Checkers, etc.)"""
    
    def calculate_score(self, game_state: Dict[str, Any], duration_seconds: int) -> Dict[str, Any]:
        """
        Default board game scoring:
        - Win: 100 points base
        - Rating/Elo adjustment based on opponent
        """
        # Subclasses can override for more complex scoring
        winner = game_state.get('winner')
        return {
            'score_value': 100 if winner else 50,
            'score_breakdown': {
                'game_outcome': 'win' if winner else 'loss_or_draw',
                'duration_seconds': duration_seconds
            }
        }


class PuzzleGameAdapter(GameAdapter):
    """Base class for puzzle games (Tetris, Candycrush, etc.)"""
    
    def calculate_score(self, game_state: Dict[str, Any], duration_seconds: int) -> Dict[str, Any]:
        """
        Default puzzle game scoring:
        - Based on level, lines/pieces cleared, combos
        """
        level = game_state.get('level', 1)
        base_score = game_state.get('points', 0)
        level_multiplier = 1 + (level - 1) * 0.1
        
        return {
            'score_value': base_score * level_multiplier,
            'score_breakdown': {
                'base_points': base_score,
                'level': level,
                'level_multiplier': level_multiplier,
                'final_score': base_score * level_multiplier
            }
        }
