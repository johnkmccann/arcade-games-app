# Complete Workflows - User & Developer Scenarios

## End-to-End: User Playing a Game

### 1. User Discovers Games

**User Flow:**
```
User opens app
    ↓
Frontend: GET /games?user_id=alice
    ↓
Backend: GameRegistry.list_all() → filters by access
    ↓
Returns: [
  {id: 'chess', title: 'Chess', ...},
  {id: 'tetris', title: 'Tetris', ...},
  {id: 'pacman', title: 'Pac-Man', ...}
]
    ↓
UI: Display game cards with "Play" button
```

**Backend Processing:**
```python
@router.get("/games")
async def get_available_games(user_id: Optional[str] = None):
    games = GameRegistry.list_all()  # [ChessMetadata, TetrisMetadata, ...]
    
    if user_id:
        # Filter by user access
        access_control = GameAccessControl(db)
        games = [
            g for g in games 
            if await access_control.can_play_game(user_id, g.id)
        ]
    
    return games  # GameMetadata objects
```

### 2. User Starts a Game

**User Flow:**
```
User clicks "Play" on Chess card
    ↓
Frontend: POST /games/chess/start
    body: {user_id: 'alice', difficulty: 'intermediate'}
    ↓
Backend: Creates GameSession
    ↓
Returns: {
  id: 'session_abc123',
  game_id: 'chess',
  user_id: 'alice',
  status: 'in_progress',
  game_state: {
    fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
    moves: [],
    current_player: 'white'
  }
}
    ↓
UI: Render ChessRenderer with game_state
```

**Backend Processing:**
```python
@router.post("/games/{game_id}/start")
async def start_game(game_id: str, user_id: str, difficulty: str = None):
    # 1. Validate access
    access_control = GameAccessControl(db)
    if not await access_control.can_play_game(user_id, game_id):
        raise HTTPException(403, "Access denied")
    
    # 2. Get adapter
    adapter = GameRegistry.get(game_id)
    if not adapter:
        raise HTTPException(404, "Game not found")
    
    # 3. Create session
    service = GameSessionService(db)
    session = await service.start_game(user_id, game_id, difficulty)
    
    return session
```

**GameSessionService Processing:**
```python
async def start_game(self, user_id, game_id, difficulty):
    adapter = GameRegistry.get(game_id)
    
    # Let Chess adapter initialize its state
    game_state = adapter.create_new_game(user_id, difficulty)
    # Returns: {fen, moves, current_player} - Chess-specific
    
    # Create session
    session = GameSession(
        user_id=user_id,
        game_id=game_id,
        game_state=game_state
    )
    
    # Save to MongoDB
    result = await self.db.game_sessions.insert_one(session.dict())
    session.id = str(result.inserted_id)
    
    return session
```

### 3. User Makes a Move

**User Flow:**
```
User clicks square e2, then e4 (in Chess)
    ↓
Frontend: POST /games/chess/sessions/session_abc123/move
    body: {from: 'e2', to: 'e4'}
    ↓
Backend: Validates & processes move
    ↓
Returns: {
  session: {..., game_state: {...updated...}},
  is_game_over: false,
  winner: null
}
    ↓
UI: Chess board updates with new position
```

**Backend Processing:**
```python
@router.post("/games/{game_id}/sessions/{session_id}/move")
async def make_move(game_id: str, session_id: str, move: dict):
    service = GameSessionService(db)
    
    # 1. Get current session
    session = await service.get_session(session_id)
    if session.status != "in_progress":
        raise HTTPException(400, "Game not active")
    
    # 2. Get adapter & process move
    adapter = GameRegistry.get(session.game_id)
    try:
        updated_state = adapter.process_move(session.game_state, move)
    except ValueError as e:
        raise HTTPException(400, f"Invalid move: {e}")
    
    # 3. Check if game over
    is_over, winner = adapter.is_game_over(updated_state)
    
    # 4. If over, calculate score
    if is_over:
        session.status = "completed"
        session.completed_at = datetime.utcnow()
        duration = (session.completed_at - session.started_at).total_seconds()
        score_data = adapter.calculate_score(updated_state, duration)
        session.score = score_data['score_value']
        session.score_breakdown = score_data['score_breakdown']
    
    session.game_state = updated_state
    
    # 5. Persist to MongoDB
    await db.game_sessions.update_one(
        {"_id": session_id},
        {"$set": session.dict()}
    )
    
    return {
        "session": session,
        "is_game_over": is_over,
        "winner": winner
    }
```

### 4. Game Ends & Score is Saved

**User Flow:**
```
Checkmate - Black wins!
    ↓
Frontend detects: is_game_over = true
    ↓
Shows: "You lost!" + score: 125
    ↓
User clicks "Save Score"
    ↓
Frontend: POST /games/chess/sessions/session_abc123/finish
    ↓
Backend: Saves score to leaderboard
```

### 5. User Views Leaderboard

**User Flow:**
```
User clicks "Leaderboard"
    ↓
Frontend: GET /games/chess/leaderboard?time_period=weekly
    ↓
Backend: Aggregates scores from leaderboard
    ↓
Returns ranked list with user's position
```

## Example: Adding Checkers Game

### 1. Developer Creates Adapter

**File: `app/services/games/checkers.py`**
```python
class CheckersAdapter(BoardGameAdapter):
    def get_metadata(self):
        return GameMetadata(
            id="checkers",
            title="Checkers",
            ...
        )
    
    def create_new_game(self, user_id, difficulty=None):
        return {'board': STARTING_POSITION, ...}
    
    def process_move(self, game_state, move):
        # Validate and apply
        return updated_state
    
    # ... all required methods
```

**Time:** 2-4 hours

### 2. Developer Registers

**File: `app/services/games/__init__.py`** (add 1 line):
```python
GameRegistry.register('checkers', CheckersAdapter())
```

### 3. Game is Available

✅ Immediately works with all endpoints:
- `GET /games` - Shows Checkers
- `POST /games/checkers/start` - Start game
- `POST /games/checkers/sessions/{id}/move` - Play
- `GET /games/checkers/leaderboard` - Rankings

**Zero changes** to existing games!

## Admin Workflows

### Set Parental Controls

```python
# Only allow specific games
user = User(
    id="child123",
    restricted_games=True,
    accessible_game_ids=["tetris", "pacman"]
)

# Child can ONLY play Tetris and Pac-Man
# Chess will be blocked
```

### Set Age Restrictions

```python
# Mark game as teen+
await access_control.set_game_age_requirement("violent_game", "teen")

# Automatically blocks: children
# Automatically allows: teens, adults
```

## Data Flows Summary

| Operation | Path | Database |
|-----------|------|----------|
| **Browse games** | API → Registry | Read |
| **Start game** | API → Adapter | INSERT session |
| **Make move** | API → Adapter | UPDATE session |
| **Finish** | API → Score calc | UPDATE session, INSERT score |
| **Leaderboard** | API → Aggregation | Pipeline query |
| **Check access** | API → Rules | Query users |

---

**Key Result:** Same API handles any game. Add Chess, Tetris, Checkers, 100+ others with *zero* framework changes.
