"""Chess game adapter implementation"""

from typing import Dict, Any, Optional
from app.models.game import GameMetadata
from app.services.game_adapter import BoardGameAdapter


class ChessAdapter(BoardGameAdapter):
    """Chess game implementation"""
    
    def get_metadata(self) -> GameMetadata:
        return GameMetadata(
            id="chess",
            title="Chess",
            genre="Strategy",
            description="Classic chess - the game of kings",
            developer="N/A",
            game_type="boardgame",
            min_players=2,
            max_players=2,
            avg_playtime_minutes=30,
            scoring_type="points",
            scoring_direction="higher_better"
        )
    
    def create_new_game(self, user_id: str, difficulty: Optional[str] = None) -> Dict[str, Any]:
        """Initialize chess game state - using FEN notation for board state"""
        return {
            'fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',  # Starting position
            'moves': [],
            'current_player': 'white',
            'status': 'active',
            'game_started_at': None,
            'captures': {'white': [], 'black': []},
            'difficulty': difficulty or 'human'
        }
    
    def process_move(self, game_state: Dict[str, Any], move: Dict[str, Any]) -> Dict[str, Any]:
        """Process a chess move"""
        # In real implementation, validate against legal moves
        from_square = move.get('from')
        to_square = move.get('to')
        promotion = move.get('promotion')
        
        if not from_square or not to_square:
            raise ValueError("Move must have 'from' and 'to' squares")
        
        # Add to move history
        game_state['moves'].append({
            'from': from_square,
            'to': to_square,
            'promotion': promotion
        })
        
        # Toggle current player
        game_state['current_player'] = 'black' if game_state['current_player'] == 'white' else 'white'
        
        return game_state
    
    def is_game_over(self, game_state: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Check for checkmate, stalemate, or draw conditions"""
        # Simplified - in reality, check board state
        game_status = game_state.get('status')
        if game_status in ['checkmate', 'stalemate', 'draw']:
            if game_status == 'checkmate':
                winner = 'black' if game_state['current_player'] == 'white' else 'white'
                return True, winner
            return True, None
        return False, None
    
    def calculate_score(self, game_state: Dict[str, Any], duration_seconds: int) -> Dict[str, Any]:
        """Chess scoring based on game outcome and time"""
        moves_count = len(game_state.get('moves', []))
        return {
            'score_value': 100 + (moves_count * 2),  # More points for longer games
            'score_breakdown': {
                'victory_bonus': 100,
                'moves': moves_count,
                'move_points': moves_count * 2,
                'duration_seconds': duration_seconds
            }
        }
    
    def validate_game_state(self, game_state: Dict[str, Any]) -> bool:
        """Validate chess state is well-formed"""
        return 'fen' in game_state and 'moves' in game_state and 'current_player' in game_state
