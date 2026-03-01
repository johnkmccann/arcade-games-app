# Quick Reference Card

## Game Adapter Interface

```python
class GameAdapter(ABC):
    @abstractmethod
    def get_metadata(self) -> GameMetadata:
        """Return game metadata (title, genre, scoring info, etc)"""
    
    @abstractmethod
    def create_new_game(self, user_id: str, difficulty: Optional[str]) -> Dict[str, Any]:
        """Initialize game_state for a new game"""
    
    @abstractmethod
    def process_move(self, game_state: Dict[str, Any], move: Dict[str, Any]) -> Dict[str, Any]:
        """Apply move to game_state, return updated state"""
    
    @abstractmethod
    def is_game_over(self, game_state: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Return (is_game_over: bool, winner_id: str or None)"""
    
    @abstractmethod
    def calculate_score(self, game_state: Dict[str, Any], duration_seconds: int) -> Dict[str, Any]:
        """Return {'score_value': 150, 'score_breakdown': {...}}"""
    
    @abstractmethod
    def validate_game_state(self, game_state: Dict[str, Any]) -> bool:
        """Return True if state is valid (for persistence recovery)"""
```

## Adding a Game in 3 Steps

### 1. Create Adapter
```bash
touch app/services/games/my_game.py
```

```python
from app.services.game_adapter import PuzzleGameAdapter  # or ArcsdeGameAdapter, BoardGameAdapter
from app.models.game import GameMetadata

class MyGameAdapter(PuzzleGameAdapter):
    def get_metadata(self):
        return GameMetadata(
            id="my_game",
            title="My Game",
            genre="Puzzle",
            game_type="puzzle",
            scoring_type="points",
            scoring_direction="higher_better"
        )
    
    def create_new_game(self, user_id, difficulty=None):
        return {
            'board': [],
            'score': 0,
            'level': 1
        }
    
    def process_move(self, game_state, move):
        # Update game_state based on move
        return game_state
    
    def is_game_over(self, game_state):
        return False, None
    
    def calculate_score(self, game_state, duration_seconds):
        return {
            'score_value': game_state['score'],
            'score_breakdown': {...}
        }
    
    def validate_game_state(self, game_state):
        return 'board' in game_state
```

### 2. Register
Edit `app/services/games/__init__.py`, add to `register_default_games()`:
```python
GameRegistry.register('my_game', MyGameAdapter())
```

### 3. Frontend Renderer (Optional)
Create `src/games/my_game/MyGameRenderer.tsx`:
```typescript
export const MyGameRenderer: React.FC<Props> = ({ state, onMove }) => {
    return <div>Render game here</div>
}
```

## API Endpoints

### Discovery
- `GET /games` - List all available games
- `GET /games/{game_id}` - Get game metadata

### Sessions
- `POST /games/{game_id}/start?user_id=X&difficulty=easy` - Start game
- `GET /games/{game_id}/sessions/{session_id}` - Get current state
- `POST /games/{game_id}/sessions/{session_id}/move` - Make move
- `POST /games/{game_id}/sessions/{session_id}/finish` - Save & finish

### Leaderboards
- `GET /games/{game_id}/leaderboard?time_period=all_time` - Global rankings
- `GET /games/{game_id}/leaderboard/friends?user_id=X` - Friend rankings
- `GET /games/{game_id}/user/{user_id}/stats` - Personal stats
- `GET /games/{game_id}/user/{user_id}/history` - Past games

## Built-in Games

The platform comes with example game implementations:

### Chess (`chess`)
- **Type:** Board Game (2 players)
- **State:** FEN notation + move history
- **Move Format:** `{"from": "e2", "to": "e4", "promotion": "q"}`
- **Lines of Code:** ~150

### Tetris (`tetris`)
- **Type:** Arcade (1 player)
- **State:** Grid + current piece + level
- **Move Format:** `{"direction": "left|right|down", "rotate": true}`
- **Scoring:** Points multiplied by level
- **Lines of Code:** ~120

### Pac-Man (`pacman`)
- **Type:** Arcade (1 player)
- **State:** Position + ghost positions + pellets
- **Move Format:** `{"direction": "up|down|left|right"}`
- **Scoring:** 10 points per pellet + ghost bonuses
- **Lines of Code:** ~130

### Darts (`darts`) - **Score Tracking Example**
- **Type:** Sport/Arcade (2-8 players)
- **State:** Player scores + turn history
- **Move Format:** `{"dart_score": 20, "is_final": false}`
- **Rules:** 
  - Start at 501 points
  - Players take 3 darts per turn
  - Dart scores subtracted from total
  - Going below zero = bust (score unchanged)
  - Final dart must be double or 50
  - First to exactly zero wins
- **Scoring:** 1000 for winner + speed bonus, other players get points for proximity to zero
- **Lines of Code:** ~300
- **Why it matters:** Shows the adapter pattern works for score-tracking games (not just board games with complex state)

## Data Models

### GameMetadata
```python
GameMetadata(
    id="chess",                    # Unique identifier
    title="Chess",                # Display name
    genre="Strategy",
    game_type="boardgame",        # boardgame, arcade, puzzle
    min_players=2,
    max_players=2,
    scoring_type="points",        # points, time, rating, custom
    scoring_direction="higher_better"
)
```

### GameSession
```python
GameSession(
    id="session_123",
    user_id="user_456",
    game_id="chess",
    status="in_progress",         # in_progress, completed, abandoned
    game_state={...},             # Game-specific state
    score=150,                    # Final score (if complete)
    score_breakdown={...}         # Score details
)
```

### Score (Leaderboard Entry)
```python
Score(
    user_id="user_456",
    game_id="chess",
    score_value=150,
    score_type="points",
    score_breakdown={
        "base_points": 100,
        "moves": 42,
        "bonus": 50
    },
    is_record=True,               # Personal best?
)
```

### User (with Access Control)
```python
User(
    id="user_456",
    username="alice",
    email="alice@example.com",
    
    # Access control
    restricted_games=False,       # If True, only accessible_game_ids
    accessible_game_ids=[],       # Whitelist when restricted=True
    age_group="adult",            # child, teen, adult
    
    # Social
    favorite_game_ids=["chess"],
    friend_ids=["user_789"],
    
    # Progress
    current_game_session_id=None  # Resume game support
)
```

## GameRegistry

```python
from app.services.game_adapter import GameRegistry

# Register game
GameRegistry.register('my_game', MyGameAdapter())

# Get specific game
adapter = GameRegistry.get('my_game')

# Get all games
all_metadata = GameRegistry.list_all()

# Check if registered
if GameRegistry.is_registered('my_game'):
    # ...
```

## Access Control

### Whitelist Mode (Parental Controls)
```python
user.restricted_games = True
user.accessible_game_ids = ['chess', 'tetris']
# User can ONLY play chess and tetris

await access_control.set_game_access(user_id, ['chess', 'tetris'])
```

### Age-Based Restrictions
```python
user.age_group = 'child'
game_access_rules['violent_game'].required_min_age = 'teen'

# Result: child cannot play violent_game
if not await access_control.can_play_game(user_id, 'violent_game'):
    raise HTTPException(403, "Too young")
```

## Leaderboard Queries

### Global (All-Time Top 100)
```python
leaderboard = await leaderboard_service.get_global_leaderboard(
    game_id='tetris',
    time_period='all_time',  # or 'weekly', 'daily'
    limit=100
)
```

### Friends Only
```python
leaderboard = await leaderboard_service.get_friend_leaderboard(
    user_id='user_456',
    game_id='tetris'
)
```

### Personal Stats
```python
stats = await leaderboard_service.get_user_game_stats('user_456', 'tetris')
# Returns: {
#   best_score: 42500,
#   average_score: 28000,
#   total_plays: 45,
#   rank: 12,
#   last_played: datetime
# }
```

## Game Session Workflow

### Start Game
```python
service = GameSessionService(db_client)
session = await service.start_game(
    user_id='player1',
    game_id='chess',
    difficulty='intermediate'
)
# session.game_state now contains initialized state
```

### Make Move
```python
session, is_over, winner = await service.process_move(
    session_id='session_123',
    move={'from': 'e2', 'to': 'e4'}
)

if is_over:
    print(f"Game over! Winner: {winner}")
    print(f"Final score: {session.score}")
```

### Resume Unfinished Game
```python
unfinished = await service.get_unfinished_games(user_id='player1')
if unfinished:
    session = unfinished[0]
    # Continue from current game_state
```

### Finish & Save
```python
session = await service.save_and_finish_game(session_id='session_123')
# Automatically saves score to leaderboard
```

## Frontend Hook Examples

### Get Available Games
```typescript
const [games, setGames] = useState<GameMetadata[]>([]);

useEffect(() => {
    api.get('/games?user_id=current_user').then(r => setGames(r.data));
}, []);
```

### Start Game
```typescript
const handlePlay = async () => {
    const response = await api.post(`/games/${gameId}/start`, {
        user_id: currentUserId
    });
    setSessionId(response.data.id);
};
```

### Make Move
```typescript
const handleSquareClick = async (square) => {
    await api.post(
        `/games/${gameId}/sessions/${sessionId}/move`,
        { from: selectedSquare, to: square }
    );
};
```

### Get Leaderboard
```typescript
const [leaderboard, setLeaderboard] = useState([]);

useEffect(() => {
    api.get(`/games/${gameId}/leaderboard?time_period=weekly&limit=100`)
        .then(r => setLeaderboard(r.data.leaderboard));
}, [gameId]);
```

## Testing Pattern

```python
def test_my_game():
    adapter = MyGameAdapter()
    
    # Create game
    state = adapter.create_new_game('user123')
    assert adapter.validate_game_state(state)
    
    # Make moves
    state = adapter.process_move(state, {'action': 'move'})
    
    # Check end condition
    is_over, winner = adapter.is_game_over(state)
    
    # Score
    score_data = adapter.calculate_score(state, 600)
    assert score_data['score_value'] > 0
```

## Common Patterns

### Arcadeish Game Scoring
```python
# Points + time bonus
base_points = game_state.get('points', 0)
time_bonus = max(0, (300 - duration) * 10)
total = base_points + time_bonus
```

### Puzzle Game Scoring
```python
# Points multiplied by level
level = game_state.get('level', 1)
base = game_state.get('points', 0)
total = base * (1 + (level - 1) * 0.1)
```

### Board Game Scoring
```python
# Win bonuses, maybe rating adjustment
if winner:
    return 100 + opponent_rating_adjustment
else:
    return 50
```

## Critical Checklist When Adding Game

- [ ] Adapter implements all abstract methods
- [ ] `get_metadata()` has correct game_id
- [ ] `create_new_game()` returns valid state
- [ ] `process_move()` validates moves raise ValueError on invalid
- [ ] `is_game_over()` detects win/draw/loss correctly
- [ ] `calculate_score()` returns score_value and breakdown
- [ ] `validate_game_state()` can detect corrupted state
- [ ] Game registered in `register_default_games()`
- [ ] Added tests in `tests/test_<game>.py`
- [ ] Frontend renderer added (optional but recommended)
