# Adding a New Game - Developer Guide

## Quick Start

Adding a new game to the platform requires only:
1. Create a single adapter class
2. Register it at startup
3. Done - game is immediately available

No existing code needs to be modified.

## Step-by-Step Example: Adding Checkers

### 1. Create the Adapter

Create `app/services/games/checkers.py`:

```python
from app.models.game import GameMetadata
from app.services.game_adapter import BoardGameAdapter
from typing import Dict, Any, Optional, Tuple

class CheckersAdapter(BoardGameAdapter):
    """Checkers board game implementation"""
    
    def get_metadata(self) -> GameMetadata:
        """Describe the game itself"""
        return GameMetadata(
            id="checkers",
            title="Checkers",
            genre="Strategy",
            description="Classic checkers - jump your pieces to victory",
            developer="Anonymous",
            game_type="boardgame",
            min_players=2,
            max_players=2,
            avg_playtime_minutes=20,
            scoring_type="points",
            scoring_direction="higher_better"
        )
    
    def create_new_game(self, user_id: str, difficulty: Optional[str] = None) -> Dict[str, Any]:
        """Initialize a new checkers game"""
        # Standard checkers starting position
        board = [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 0],
        ]
        # 0 = empty, 1 = red piece, 2 = black piece
        # 10 = red king, 20 = black king
        
        return {
            'board': board,
            'current_player': 'red',  # Start with red
            'red_pieces': 12,
            'black_pieces': 12,
            'move_history': [],
            'jumped_pieces': 0,
            'kings_created': 0,
            'difficulty': difficulty or 'normal',
            'game_status': 'active'
        }
    
    def process_move(self, game_state: Dict[str, Any], move: Dict[str, Any]) -> Dict[str, Any]:
        """Process a checker move"""
        from_pos = move.get('from')  # (row, col)
        to_pos = move.get('to')      # (row, col)
        
        if not from_pos or not to_pos:
            raise ValueError("Move must have 'from' and 'to' positions")
        
        # Validate the move is legal
        if not self._is_legal_move(game_state, from_pos, to_pos):
            raise ValueError(f"Illegal move from {from_pos} to {to_pos}")
        
        # Execute the move
        board = game_state['board']
        piece = board[from_pos[0]][from_pos[1]]
        board[to_pos[0]][to_pos[1]] = piece
        board[from_pos[0]][from_pos[1]] = 0
        
        # Check for jump/capture
        jumped = self._check_jump(from_pos, to_pos)
        if jumped:
            jumped_row, jumped_col = jumped
            opponent_piece = board[jumped_row][jumped_col]
            board[jumped_row][jumped_col] = 0
            
            if piece % 10 == 1:  # Red piece
                game_state['black_pieces'] -= 1
            else:  # Black piece
                game_state['red_pieces'] -= 1
            
            game_state['jumped_pieces'] += 1
        
        # Check for king
        if piece == 1 and to_pos[0] == 7:  # Red reaches back row
            board[to_pos[0]][to_pos[1]] = 10
            game_state['kings_created'] += 1
        elif piece == 2 and to_pos[0] == 0:  # Black reaches back row
            board[to_pos[0]][to_pos[1]] = 20
            game_state['kings_created'] += 1
        
        # Record move
        game_state['move_history'].append({
            'from': from_pos,
            'to': to_pos,
            'jumped': jumped
        })
        
        # Toggle player
        game_state['current_player'] = 'black' if game_state['current_player'] == 'red' else 'red'
        
        return game_state
    
    def is_game_over(self, game_state: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Check if game is over (no pieces or no legal moves)"""
        if game_state['red_pieces'] == 0:
            return True, 'black'
        if game_state['black_pieces'] == 0:
            return True, 'red'
        
        # Check for stalemate (current player has no legal moves)
        if not self._has_legal_moves(game_state):
            other_player = 'black' if game_state['current_player'] == 'red' else 'red'
            return True, other_player
        
        return False, None
    
    def calculate_score(self, game_state: Dict[str, Any], duration_seconds: int) -> Dict[str, Any]:
        """Checkers scoring"""
        # Pieces remaining + time bonus
        pieces_value = 50 * game_state['red_pieces']  # Pieces on board
        kings_value = game_state['kings_created'] * 25
        jumps_value = game_state['jumped_pieces'] * 10
        
        total = pieces_value + kings_value + jumps_value
        
        return {
            'score_value': total,
            'score_breakdown': {
                'pieces_on_board': game_state['red_pieces'],
                'pieces_value': pieces_value,
                'kings_created': game_state['kings_created'],
                'kings_value': kings_value,
                'pieces_jumped': game_state['jumped_pieces'],
                'jumps_value': jumps_value,
                'moves': len(game_state['move_history']),
                'duration_seconds': duration_seconds,
                'total_score': total
            }
        }
    
    def validate_game_state(self, game_state: Dict[str, Any]) -> bool:
        """Validate checkers state"""
        required = ['board', 'current_player', 'red_pieces', 'black_pieces']
        return all(field in game_state for field in required)
    
    def get_legal_moves(self, game_state: Dict[str, Any]) -> list[Dict[str, Any]]:
        """Return list of legal moves from current position"""
        moves = []
        current = game_state['current_player']
        board = game_state['board']
        
        # Find pieces of current player
        piece_type = 1 if current == 'red' else 2
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece % 10 != piece_type:
                    continue
                
                # Check all possible moves for this piece
                # Regular moves (diagonal 1 square)
                for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if board[new_row][new_col] == 0:
                            moves.append({
                                'from': (row, col),
                                'to': (new_row, new_col),
                                'type': 'normal'
                            })
                
                # Jump moves (diagonal 2 squares with capture)
                for dr, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                    new_row, new_col = row + dr, col + dc
                    jumped_row = row + dr // 2
                    jumped_col = col + dc // 2
                    
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if board[new_row][new_col] == 0:
                            opponent = board[jumped_row][jumped_col]
                            if opponent > 0 and opponent % 10 != piece_type:
                                moves.append({
                                    'from': (row, col),
                                    'to': (new_row, new_col),
                                    'type': 'jump'
                                })
        
        return moves
    
    # Helper methods
    
    def _is_legal_move(self, game_state: Dict[str, Any], from_pos, to_pos) -> bool:
        """Check if a move is legal"""
        legal_moves = self.get_legal_moves(game_state)
        return any(
            m['from'] == from_pos and m['to'] == to_pos
            for m in legal_moves
        )
    
    def _check_jump(self, from_pos, to_pos) -> Optional[tuple]:
        """If this is a jump move, return the position jumped over"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        
        # Jump is 2 squares diagonal
        if row_diff == 2 and col_diff == 2:
            jumped_row = (from_row + to_row) // 2
            jumped_col = (from_col + to_col) // 2
            return (jumped_row, jumped_col)
        
        return None
    
    def _has_legal_moves(self, game_state: Dict[str, Any]) -> bool:
        """Check if current player has any legal moves"""
        return len(self.get_legal_moves(game_state)) > 0
```

### 2. Register the Game

In `app/services/games/__init__.py`, add to `register_default_games()`:

```python
def register_default_games():
    """Register the default games that come with the platform"""
    from app.services.game_adapter import GameRegistry
    from app.services.games.checkers import CheckersAdapter
    
    GameRegistry.register('chess', ChessAdapter())
    GameRegistry.register('tetris', TetrisAdapter())
    GameRegistry.register('pacman', PacManAdapter())
    GameRegistry.register('checkers', CheckersAdapter())  # ← Add this
```

### 3. Call Registration at Startup

In `app/main.py`:

```python
from fastapi import FastAPI
from app.services.games import register_default_games

app = FastAPI()

# Register all games
register_default_games()

# ... rest of app setup
```

### 4. Done!

Your game is now immediately available:

```bash
# List all games
curl http://localhost:8000/api/v1/games

# Get game metadata
curl http://localhost:8000/api/v1/games/checkers

# Start a game
curl -X POST http://localhost:8000/api/v1/games/checkers/start \
  -H "Content-Type: application/json" \
  -d '{"user_id": "player1", "difficulty": "intermediate"}'

# Make a move
curl -X POST http://localhost:8000/api/v1/games/checkers/sessions/{sessionId}/move \
  -H "Content-Type: application/json" \
  -d '{"from": [5, 1], "to": [4, 0]}'
```

## Designing Your Game State

The key to making a scalable game is deciding what goes in `game_state`. It should be:

1. **Minimal but complete** - just enough to resume the game
2. **JSON-serializable** - must store in MongoDB
3. **Deterministic** - given state + moves, outcome is predictable

### Examples

**Chess:**
```python
game_state = {
    'fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
    'moves': ['e2e4', 'c7c5'],
    'current_player': 'white'
}
```
Replay: Start from FEN, replay moves → any position

**Tetris:**
```python
game_state = {
    'board': [[0]*10 for _ in range(20)],
    'current_piece': {'type': 'T', 'x': 4, 'y': 0, 'rotation': 0},
    'next_piece': {'type': 'I', ...},
    'level': 3,
    'points': 4250,
    'lines_cleared': 12
}
```
Replay: Recreate board, continue falling pieces

**Poker:**
```python
game_state = {
    'players': ['alice', 'bob'],
    'hole_cards': {'alice': ['AH', 'KH'], 'bob': ['2C', '3D']},
    'community_cards': ['AC', 'AS', 'AD'],
    'pot': 150,
    'current_bet': 50,
    'whose_turn': 'bob',
    'action_history': [...]
}
```

## Important Patterns

### 1. Always validate moves

```python
def process_move(self, game_state, move):
    from_pos = move.get('from')
    to_pos = move.get('to')
    
    if not from_pos or not to_pos:
        raise ValueError("Both 'from' and 'to' required")
    
    # Don't assume move is valid - validate it!
    if not self._is_legal_move(game_state, from_pos, to_pos):
        raise ValueError(f"Illegal move from {from_pos} to {to_pos}")
    
    # Process move...
```

### 2. Use helper methods

```python
def is_game_over(self, game_state):
    if self._player_has_no_pieces(game_state):
        return True, None
    
    if self._is_stalemate(game_state):
        return True, None
    
    return False, None
```

### 3. Make `score_breakdown` detailed

```python
return {
    'score_value': 1250,
    'score_breakdown': {
        'pieces_captured': 5,
        'capture_points': 500,
        'level': 3,
        'level_bonus': 750,
        'time_played_seconds': 300,
        'fastest_finish_bonus': 0,
        'total': 1250
    }
}
```

This helps users understand their score and makes leaderboards more interesting.

## Optional: AI Opponent

If your game supports single-player AI:

```python
def get_ai_move(self, game_state: Dict[str, Any], difficulty: str = "medium") -> Dict[str, Any]:
    """Return an AI move at the given difficulty level"""
    
    if difficulty == "easy":
        # Random legal move
        moves = self.get_legal_moves(game_state)
        return random.choice(moves) if moves else None
    
    elif difficulty == "medium":
        # Simple heuristics
        moves = self.get_legal_moves(game_state)
        best_move = None
        best_score = -float('inf')
        
        for move in moves:
            test_state = deepcopy(game_state)
            test_state = self.process_move(test_state, move)
            score = self._evaluate_position(test_state)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    elif difficulty == "hard":
        # Minimax or sophisticated algorithm
        return self._minimax(game_state, depth=6)
```

## Testing Your Adapter

Create `tests/test_checkers.py`:

```python
import pytest
from app.services.games.checkers import CheckersAdapter

@pytest.fixture
def adapter():
    return CheckersAdapter()

def test_new_game_initialization(adapter):
    """Test that new game initializes correctly"""
    state = adapter.create_new_game("user123")
    
    assert state['current_player'] == 'red'
    assert state['red_pieces'] == 12
    assert state['black_pieces'] == 12
    assert adapter.validate_game_state(state)

def test_legal_move(adapter):
    """Test that valid move is accepted"""
    state = adapter.create_new_game("user123")
    
    # Make a legal opening move
    move = {'from': (5, 1), 'to': (4, 0)}
    new_state = adapter.process_move(state, move)
    
    assert new_state['current_player'] == 'black'
    assert new_state['move_history'][0]['from'] == (5, 1)

def test_invalid_move(adapter):
    """Test that invalid move raises error"""
    state = adapter.create_new_game("user123")
    
    # Illegal move
    move = {'from': (0, 0), 'to': (2, 2)}
    with pytest.raises(ValueError):
        adapter.process_move(state, move)

def test_scoring(adapter):
    """Test score calculation"""
    state = adapter.create_new_game("user123")
    state['red_pieces'] = 8
    state['kings_created'] = 2
    state['jumped_pieces'] = 3
    
    score_data = adapter.calculate_score(state, 600)
    
    assert score_data['score_value'] > 0
    assert 'score_breakdown' in score_data
```

Run tests:
```bash
pytest tests/test_checkers.py -v
```

## Summary

Adding a new game is:
1. ✅ Create one adapter class (~300-500 lines for complex game)
2. ✅ Register it (1 line in `__init__.py`)
3. ✅ Call `register_default_games()` at startup (already done)
4. ✅ Game is immediately available

**Total time to add a game:** 2-4 hours for a moderately complex game, once you understand the adapter pattern.

**Impact on existing code:** Zero - completely independent.

This is what makes the platform truly scalable.

## Another Example: The Darts Game

The platform includes a **Darts** implementation that demonstrates a different game category: **score tracking games** where the app manages scores but gameplay happens on physical hardware.

### Why Darts?

Unlike board games like Chess or Checkers, Darts is:
- **Simpler to implement:** ~300 lines vs 500+ for complex board games
- **Different game flow:** Players take 3-dart turns, not individual moves
- **Different win condition:** First to reach exactly 0 (not capture pieces)
- **Different state format:** Tracks turn history and player scores, no complex board representation

This shows that the adapter pattern works for ANY game type, not just traditional board games.

### How Darts Works

**Game State:**
```python
{
    'players': [
        {'user_id': 'alice', 'score': 501, 'status': 'active'},
        {'user_id': 'bob', 'score': 501, 'status': 'active'}
    ],
    'current_player_index': 0,
    'turn_darts': [20, 20, 15],  # Darts thrown this turn
    'turn_start_score': 501,      # For bust detection
    'history': [ ... ],            # Previous turns
    'game_status': 'active'
}
```

**A Move:**
```python
move = {'dart_score': 20, 'is_final': False}  # Player just threw a 20
```

The adapter handles:
- ✅ Validating dart scores (0, 1-20 single, 2-40 double, 3-60 triple, 25, 50)
- ✅ Detecting busts (going below zero, score reverts)
- ✅ Ensuring final dart is a finishing dart (double or 50)
- ✅ Rotating players between turns
- ✅ Detecting winner (first to exactly 0)
- ✅ Scoring (1000 for winner + speed bonus, other players get points for how close they got)

### Key Code from DartsAdapter

```python
class DartsAdapter(GameAdapter):
    def process_move(self, game_state: Dict[str, Any], move: Dict[str, Any]) -> Dict[str, Any]:
        """Process a dart being entered"""
        dart_score = move.get('dart_score')
        
        # Validate dart
        if not self._is_valid_dart(dart_score):
            return game_state
        
        game_state['turn_darts'].append(dart_score)
        
        # When 3 darts thrown, resolve the turn
        if len(game_state['turn_darts']) == 3:
            subtotal = sum(game_state['turn_darts'])
            new_score = game_state['turn_start_score'] - subtotal
            
            if new_score < 0:
                # Bust! Keep old score
                game_state['history'].append({
                    'darts': game_state['turn_darts'],
                    'end_score': game_state['turn_start_score'],
                    'busted': True
                })
            elif new_score == 0 and self._is_finishing_dart(game_state['turn_darts'][-1]):
                # Winner!
                current_player['score'] = 0
                game_state['winner_user_id'] = current_player['user_id']
                game_state['game_status'] = 'finished'
            else:
                # Normal turn
                current_player['score'] = new_score
                game_state['history'].append({
                    'darts': game_state['turn_darts'],
                    'end_score': new_score,
                    'busted': False
                })
            
            # Next player's turn
            game_state['current_player_index'] = (game_state['current_player_index'] + 1) % len(game_state['players'])
            game_state['turn_darts'] = []
        
        return game_state
    
    def _is_valid_dart(self, score: int) -> bool:
        """Valid dart scores"""
        return score == 0 or score in range(1, 21) or \
               score in range(2, 41, 2) or \
               score in range(3, 61, 3) or \
               score in [25, 50]
```

### Why This Matters

**Compare game implementations:**

| Aspect | Chess | Checkers | Darts |
|--------|-------|----------|-------|
| Complexity | 500+ lines | 300 lines | 300 lines |
| Board/Grid | Yes (8x8) | Yes (8x8) | No (just scores) |
| Move type | Piece movement | Piece movement | Score entry |
| State shape | Piece positions + history | Piece positions + history | Player scores + turns |
| Win condition | Checkmate/Stalemate | Capture all pieces | Reach exactly 0 |
| Turn structure | One move at a time | One move at a time | Three darts per turn |

**All work with the same GameAdapter interface.** All are registered the same way. All are queried the same way through the API. All store their state in the same `game_state` field.

This is the power of the adapter pattern: you adapt to the game's needs, not the other way around.
