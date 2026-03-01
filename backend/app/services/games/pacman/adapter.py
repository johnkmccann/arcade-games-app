"""Pac-Man game adapter implementation"""

import random
from typing import Dict, Any, Optional, List
from app.models.game import GameMetadata
from app.services.game_adapter import GameAdapter


class PacManAdapter(GameAdapter):
    """Pac-Man game implementation"""
    
    def get_metadata(self) -> GameMetadata:
        return GameMetadata(
            id="pacman",
            title="Pac-Man",
            genre="Arcade",
            description="Eat the dots and avoid the ghosts",
            developer="Namco",
            game_type="arcade",
            min_players=1,
            max_players=1,
            avg_playtime_minutes=5,
            scoring_type="points",
            scoring_direction="higher_better",
            max_score=9999
        )
    
    def create_new_game(self, user_id: str, difficulty: Optional[str] = None) -> Dict[str, Any]:
        """Initialize Pac-Man game state"""
        return {
            'pacman_pos': {'x': 10, 'y': 10},
            'ghosts': [
                {'name': 'Blinky', 'x': 9, 'y': 9, 'color': 'red'},
                {'name': 'Pinky', 'x': 10, 'y': 9, 'color': 'pink'},
                {'name': 'Inky', 'x': 11, 'y': 9, 'color': 'cyan'},
                {'name': 'Clyde', 'x': 10, 'y': 10, 'color': 'orange'}
            ],
            'dots': self._generate_dots(),
            'score': 0,
            'lives': 3,
            'level': 1,
            'game_over': False,
            'dots_eaten': 0
        }
    
    def process_move(self, game_state: Dict[str, Any], move: Dict[str, Any]) -> Dict[str, Any]:
        """Process Pac-Man movement"""
        direction = move.get('direction')  # 'up', 'down', 'left', 'right'
        pacman = game_state['pacman_pos']
        
        dx, dy = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}.get(direction, (0, 0))
        pacman['x'] = max(0, min(19, pacman['x'] + dx))
        pacman['y'] = max(0, min(19, pacman['y'] + dy))
        
        # Check if dot eaten
        if (pacman['x'], pacman['y']) in game_state['dots']:
            game_state['dots'].remove((pacman['x'], pacman['y']))
            game_state['score'] += 10
            game_state['dots_eaten'] += 1
        
        # Move ghosts (simplified AI)
        for ghost in game_state['ghosts']:
            ghost['x'] = max(0, min(19, ghost['x'] + random.randint(-1, 1)))
            ghost['y'] = max(0, min(19, ghost['y'] + random.randint(-1, 1)))
        
        return game_state
    
    def is_game_over(self, game_state: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Check if Pac-Man got caught or won"""
        if not game_state.get('dots'):  # All dots eaten
            return True, 'won'
        if game_state.get('lives', 0) <= 0:
            return True, 'lost'
        return False, None
    
    def calculate_score(self, game_state: Dict[str, Any], duration_seconds: int) -> Dict[str, Any]:
        """Pac-Man scoring"""
        return {
            'score_value': game_state.get('score', 0),
            'score_breakdown': {
                'dot_points': game_state.get('dots_eaten', 0) * 10,
                'level_bonus': game_state.get('level', 1) * 100,
                'duration_seconds': duration_seconds
            }
        }
    
    def validate_game_state(self, game_state: Dict[str, Any]) -> bool:
        """Validate Pac-Man state"""
        return all(k in game_state for k in ['pacman_pos', 'ghosts', 'score', 'lives'])
    
    def _generate_dots(self) -> List[tuple]:
        """Generate initial dot positions"""
        dots = []
        for x in range(20):
            for y in range(20):
                if (x, y) not in [(9, 9), (10, 9), (11, 9), (10, 10)]:  # Avoid ghost starting positions
                    dots.append((x, y))
        return dots
