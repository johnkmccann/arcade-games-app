"""Darts game adapter implementation"""

from typing import Dict, Any, Optional
from app.models.game import GameMetadata
from app.services.game_adapter import GameAdapter


class DartsAdapter(GameAdapter):
    """
    Darts game implementation - a score tracking game for physical dartboards.
    
    Players start with 501 points and take turns throwing 3 darts.
    Each dart's score is subtracted from their total.
    First to reach exactly zero wins.
    
    Game state stores player scores and turn history.
    Moves are dart scores entered by players after throwing physical darts.
    """
    
    def get_metadata(self) -> GameMetadata:
        return GameMetadata(
            id="darts",
            title="Darts",
            genre="Sports",
            description="Score tracking for physical dartboard games. Players throw darts and track scores.",
            developer="Classic Sport",
            game_type="arcade",
            min_players=2,
            max_players=8,
            avg_playtime_minutes=20,
            scoring_type="points",
            scoring_direction="lower_better",  # First to zero wins
            max_score=501
        )
    
    def create_new_game(self, user_id: str, difficulty: Optional[str] = None) -> Dict[str, Any]:
        """Initialize a new darts game with 501 starting points per player"""
        return {
            'players': [
                {'user_id': user_id, 'score': 501, 'status': 'active', 'busted': False}
            ],
            'current_player_index': 0,
            'turn_darts': [],  # Darts thrown in current turn (max 3)
            'turn_start_score': 501,  # Score before this turn started
            'history': [],  # List of completed turns: {player_idx, darts, start_score, end_score, busted}
            'game_status': 'active',  # 'active' or 'finished'
            'winner_user_id': None,
            'created_at': None
        }
    
    def process_move(self, game_state: Dict[str, Any], move: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a dart being thrown.
        
        Move format: {
            'dart_score': int (0-60, valid darts values),
            'is_final': bool (is this the 3rd dart of the turn?)
        }
        """
        dart_score = move.get('dart_score', 0)
        is_final = move.get('is_final', False)
        
        # Validate dart score
        if not self._is_valid_dart(dart_score):
            return game_state  # Invalid dart, ignore
        
        current_player = game_state['players'][game_state['current_player_index']]
        game_state['turn_darts'].append(dart_score)
        
        # Check if turn is complete (3 darts thrown)
        darts_in_turn = len(game_state['turn_darts'])
        
        if darts_in_turn == 3 or is_final:
            # Turn complete - resolve the turn
            turn_subtotal = sum(game_state['turn_darts'])
            new_score = game_state['turn_start_score'] - turn_subtotal
            
            # Check for bust (went below zero)
            if new_score < 0:
                # Bust! Score reverts to start of turn
                current_player['score'] = game_state['turn_start_score']
                game_state['history'].append({
                    'player_index': game_state['current_player_index'],
                    'darts': game_state['turn_darts'][:],
                    'start_score': game_state['turn_start_score'],
                    'end_score': game_state['turn_start_score'],
                    'busted': True
                })
            elif new_score == 0:
                # Winner! Final dart must be a double or 50
                if self._is_finishing_dart(game_state['turn_darts'][-1]):
                    current_player['score'] = 0
                    current_player['status'] = 'finished'
                    game_state['game_status'] = 'finished'
                    game_state['winner_user_id'] = current_player['user_id']
                else:
                    # Bust - final dart wasn't a double
                    current_player['score'] = game_state['turn_start_score']
                    game_state['history'].append({
                        'player_index': game_state['current_player_index'],
                        'darts': game_state['turn_darts'][:],
                        'start_score': game_state['turn_start_score'],
                        'end_score': game_state['turn_start_score'],
                        'busted': True
                    })
            else:
                # Valid score, update player
                current_player['score'] = new_score
                game_state['history'].append({
                    'player_index': game_state['current_player_index'],
                    'darts': game_state['turn_darts'][:],
                    'start_score': game_state['turn_start_score'],
                    'end_score': new_score,
                    'busted': False
                })
            
            # Move to next player if game not finished
            if game_state['game_status'] != 'finished':
                game_state['current_player_index'] = (game_state['current_player_index'] + 1) % len(game_state['players'])
                game_state['turn_darts'] = []
                game_state['turn_start_score'] = game_state['players'][game_state['current_player_index']]['score']
        
        return game_state
    
    def is_game_over(self, game_state: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Check if game is finished (someone reached exactly zero with finishing dart)"""
        if game_state['game_status'] == 'finished':
            return True, game_state['winner_user_id']
        return False, None
    
    def calculate_score(self, game_state: Dict[str, Any], play_duration_seconds: int) -> Dict[str, Any]:
        """
        Calculate final scores. Winner gets 1000 points + bonus for quick finish.
        Other players get points based on how close they got to zero.
        """
        scores = {}
        
        for i, player in enumerate(game_state['players']):
            user_id = player['user_id']
            if user_id == game_state['winner_user_id']:
                # Winner: 1000 base + bonus for speed (faster = more bonus)
                speed_bonus = max(0, 300 - (play_duration_seconds // 60))  # Bonus decreases with time
                scores[user_id] = 1000 + speed_bonus
            else:
                # Non-winner: points based on how close to zero (501 - remaining = points)
                points_scored = 501 - player['score']
                scores[user_id] = points_scored
        
        return scores
    
    def validate_game_state(self, game_state: Dict[str, Any]) -> bool:
        """Validate darts game state"""
        required_keys = ['players', 'current_player_index', 'turn_darts', 'turn_start_score', 'game_status']
        if not all(k in game_state for k in required_keys):
            return False
        
        # Each player should have score between 0 and 501
        for player in game_state['players']:
            if not (0 <= player['score'] <= 501):
                return False
        
        # Current player index should be valid
        if not (0 <= game_state['current_player_index'] < len(game_state['players'])):
            return False
        
        return True
    
    def add_player(self, game_state: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Add a new player to an active game (before game starts).
        Returns updated game_state.
        """
        if game_state['game_status'] != 'active':
            return game_state  # Can't add players to finished games
        
        if any(p['user_id'] == user_id for p in game_state['players']):
            return game_state  # Player already in game
        
        game_state['players'].append({
            'user_id': user_id,
            'score': 501,
            'status': 'active',
            'busted': False
        })
        
        return game_state
    
    def _is_valid_dart(self, score: int) -> bool:
        """Check if dart score is valid"""
        # Valid: 0, 1-20 (single), 2-40 (double), 3-60 (triple), 25, 50
        if score == 0:
            return True
        if 1 <= score <= 20:
            return True
        if 2 <= score <= 40 and score % 2 == 0:  # Doubles
            return True
        if 3 <= score <= 60 and score % 3 == 0:  # Triples
            return True
        if score in [25, 50]:
            return True
        return False
    
    def _is_finishing_dart(self, dart_score: int) -> bool:
        """Check if dart is a valid finishing dart (double or 50)"""
        # Must be double (2-40, divisible by 2) or 50
        if dart_score == 50:
            return True
        if 2 <= dart_score <= 40 and dart_score % 2 == 0:
            return True
        return False
