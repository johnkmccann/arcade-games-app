"""Tetris game adapter implementation"""

import random
from typing import Dict, Any, Optional, List
from app.models.game import GameMetadata
from app.services.game_adapter import PuzzleGameAdapter


class TetrisAdapter(PuzzleGameAdapter):
    """Tetris game implementation"""
    
    def get_metadata(self) -> GameMetadata:
        return GameMetadata(
            id="tetris",
            title="Tetris",
            genre="Puzzle",
            description="Stack the falling blocks to clear lines",
            developer="Alexey Pajitnov",
            game_type="arcade",
            min_players=1,
            max_players=1,
            avg_playtime_minutes=10,
            scoring_type="points",
            scoring_direction="higher_better",
            max_score=999999
        )
    
    def create_new_game(self, user_id: str, difficulty: Optional[str] = None) -> Dict[str, Any]:
        """Initialize Tetris game state"""
        return {
            'board': [[0] * 10 for _ in range(20)],  # 10x20 grid
            'current_piece': self._get_random_piece(),
            'next_piece': self._get_random_piece(),
            'score': 0,
            'level': 1,
            'lines_cleared': 0,
            'game_over': False,
            'pieces_fallen': 0
        }
    
    def process_move(self, game_state: Dict[str, Any], move: Dict[str, Any]) -> Dict[str, Any]:
        """Process a Tetris move (rotate, move left/right, drop)"""
        action = move.get('action')  # 'rotate', 'left', 'right', 'drop'
        
        if action == 'rotate':
            # Rotate current piece
            game_state['current_piece']['rotation'] = (game_state['current_piece'].get('rotation', 0) + 1) % 4
        elif action == 'left':
            game_state['current_piece']['x'] = max(0, game_state['current_piece']['x'] - 1)
        elif action == 'right':
            game_state['current_piece']['x'] = min(9, game_state['current_piece']['x'] + 1)
        elif action == 'drop':
            # In real game, piece would fall
            lines = self._clear_lines(game_state['board'])
            game_state['lines_cleared'] += lines
            game_state['level'] = 1 + game_state['lines_cleared'] // 10
            game_state['score'] = self._calculate_tetris_score(lines, game_state['level'])
            game_state['current_piece'] = game_state['next_piece']
            game_state['next_piece'] = self._get_random_piece()
            game_state['pieces_fallen'] += 1
        
        return game_state
    
    def is_game_over(self, game_state: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Check if game-over condition is met"""
        return game_state.get('game_over', False), None
    
    def validate_game_state(self, game_state: Dict[str, Any]) -> bool:
        """Validate Tetris state"""
        required_fields = ['board', 'score', 'level', 'lines_cleared']
        return all(field in game_state for field in required_fields)
    
    def _get_random_piece(self) -> Dict[str, Any]:
        """Get a random Tetris piece"""
        pieces = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
        return {
            'type': random.choice(pieces),
            'x': 5,
            'y': 0,
            'rotation': 0
        }
    
    def _clear_lines(self, board: List[List[int]]) -> int:
        """Clear completed lines"""
        cleared = 0
        for i in range(len(board)):
            if all(cell for cell in board[i]):
                board.pop(i)
                board.insert(0, [0] * 10)
                cleared += 1
        return cleared
    
    def _calculate_tetris_score(self, lines: int, level: int) -> int:
        """Calculate score for cleared lines"""
        base_scores = {1: 100, 2: 300, 3: 500, 4: 800}
        return base_scores.get(lines, 0) * level
