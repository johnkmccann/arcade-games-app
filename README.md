# Arcade Games Platform 🎮

A scalable, extensible web platform for playing various arcade games, board games, and puzzles with leaderboards, friend rankings, and user access control.

## 🌟 Key Features

### For Users
- **Game Library** - Discover and play multiple games in the browser
- **Personal Progress** - Track your best scores, play history, and unfinished games
- **Leaderboards** - Global rankings, friend leaderboards, and personal statistics
- **Social** - Add friends, see their scores, and compete
- **Flexibility** - Resume unfinished games, different difficulty levels

### For Developers
- **Adapter Pattern** - Add new games without modifying existing code
- **Generic State Management** - Each game stores state however it needs
- **Flexible Scoring** - Support for points, time, ratings, or custom scoring
- **Access Control** - Age restrictions, game whitelisting, parental controls
- **Extensible Architecture** - Easy to add features without affecting existing games

## 📚 Documentation

### Architecture & Design
- [**SCALABLE_ARCHITECTURE.md**](./docs/SCALABLE_ARCHITECTURE.md) - Complete architecture overview, design patterns, database schema, and scaling considerations
- [**ADDING_GAMES.md**](./docs/ADDING_GAMES.md) - Step-by-step guide for adding new games with code examples
- [**FRONTEND_INTEGRATION.md**](./docs/FRONTEND_INTEGRATION.md) - Frontend components, game discovery, rendering, and leaderboards

### Database
- [**DATABASE.md**](./docs/DATABASE.md) - MongoDB schema for users, games, and scores

### API
- [**API.md**](./docs/API.md) - REST API endpoint reference

## 🏗️ Architecture Highlights

### The Game Adapter Pattern

Every game implements a simple interface:

```python
class GameAdapter(ABC):
    def get_metadata(self) -> GameMetadata
    def create_new_game(user_id, difficulty) -> Dict
    def process_move(game_state, move) -> Dict
    def is_game_over(game_state) -> (bool, winner)
    def calculate_score(game_state, duration) -> Dict
    def validate_game_state(game_state) -> bool
```

This enables:
- ✅ Adding games without touching existing code
- ✅ Each game completely independent
- ✅ Different scoring systems per game
- ✅ Flexible game state storage
- ✅ Easy testing in isolation

### Generic Game State

Rather than separate collections per game, all game state is stored as:

```python
game_state: Dict[str, Any]  # Game-specific structure
```

**Chess** might store: `{fen, moves, current_player}`
**Tetris** might store: `{grid, current_piece, level, score}`
**Custom game** can store: anything needed to resume play

### Flexible Scoring

```python
score_value: 150              # The actual score
score_breakdown: {            # How it was calculated
  base_points: 100,
  multiplier: 1.5,
  bonus: 50
}
```

## 🎮 Built-in Games

- **Chess** - Classic strategy board game
- **Tetris** - Falling block puzzle
- **Pac-Man** - Arcade maze game

Adding more takes ~2-4 hours per game (implementation only, no framework changes).

## 📊 Leaderboards

### Global Leaderboard
```
All-time scores across all players
Weekly/daily competitions
Sorted by score value
```

### Friend Leaderboard
```
See how you rank vs your friends
Compare best scores
Track improvement
```

### Personal Stats
```
Best score per game
Total games played
Average score
Current rank
Play history
```

## 🔐 User Access Control

### Whitelist Mode
```python
user.restricted_games = True
user.accessible_game_ids = ['chess', 'tetris']  # Only these games
```

### Age-Based Restrictions
```python
user.age_group = 'child'  # 'child', 'teen', 'adult'
game_access_rules['game_id'].required_min_age = 'teen'
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB 5.0+
- Docker (recommended)

### Setup

1. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

2. **Frontend Setup**
```bash
cd frontend
npm install

# Create local environment configuration from example
cp .env.example .env.local
# Edit .env.local if your backend is on a different server/port
```

3. **Start Development Servers**
```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

Visit `http://localhost:5173` for the frontend.

### Environment Configuration

The frontend uses environment variables to configure the backend API URL:

- **`.env.example`** - Sample configuration (commit to git)
- **`.env.local`** - Your local configuration (git-ignored, create from `.env.example`)
- **`.env.production`** - Production configuration (git-ignored, optional)

For local development with backend on `localhost:5001`, ensure `.env.local` contains:
```
VITE_API_URL=http://localhost:5001
```

If backend is on a different machine or port, update `VITE_API_URL` accordingly. For production deployments where frontend and backend share a domain, leave it empty or unset.

## 📁 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── games.py          # Game endpoints
│   │   │       ├── users.py          # User management
│   │   │       └── scores.py         # Leaderboard endpoints
│   │   ├── models/
│   │   │   ├── game.py               # GameMetadata, GameSession
│   │   │   ├── user.py               # User, access control
│   │   │   └── score.py              # Score, leaderboard models
│   │   ├── services/
│   │   │   ├── game_adapter.py       # Adapter pattern & registry
│   │   │   ├── game_session_service.py # Session management
│   │   │   ├── leaderboard_service.py  # Leaderboard & stats
│   │   │   └── games/
│   │   │       ├── __init__.py       # Game registration
│   │   │       ├── chess.py          # Chess adapter
│   │   │       ├── tetris.py         # Tetris adapter
│   │   │       └── pacman.py         # Pac-Man adapter
│   │   └── main.py                   # FastAPI app setup
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── GameCard.tsx          # Game preview card
│   │   │   ├── GameCanvas.tsx        # Generic game renderer
│   │   │   ├── Leaderboard.tsx       # Leaderboard display
│   │   │   └── GameRenderer.tsx      # Routes to game-specific renderers
│   │   ├── games/
│   │   │   ├── chess/
│   │   │   ├── tetris/
│   │   │   └── pacman/
│   │   ├── pages/
│   │   │   ├── GameLibrary.tsx       # Browse games
│   │   │   ├── GamePlay.tsx          # Play a game
│   │   │   └── UserProfile.tsx       # User stats & history
│   │   ├── services/
│   │   │   └── api.ts                # API client
│   │   └── types/
│   │       └── index.ts              # TypeScript types
│   └── package.json
│
└── docs/
    ├── SCALABLE_ARCHITECTURE.md      # Design patterns & architecture
    ├── ADDING_GAMES.md               # How to add new games
    ├── FRONTEND_INTEGRATION.md       # Frontend components & integration
    ├── DATABASE.md                   # MongoDB schema
    ├── API.md                        # API endpoints
    └── SETUP.md                      # Installation & running
```

## 🔌 Adding a New Game

### 1. Create Adapter (~300 lines)
```python
# app/services/games/checkers.py
class CheckersAdapter(BoardGameAdapter):
    def get_metadata(self) -> GameMetadata: ...
    def create_new_game(self, user_id, difficulty) -> Dict: ...
    def process_move(self, game_state, move) -> Dict: ...
    def is_game_over(self, game_state): ...
    def calculate_score(self, game_state, duration) -> Dict: ...
    def validate_game_state(self, game_state) -> bool: ...
```

### 2. Register at Startup (1 line)
```python
# app/services/games/__init__.py
GameRegistry.register('checkers', CheckersAdapter())
```

### 3. Create Frontend Renderer (optional)
```typescript
// src/games/checkers/CheckersRenderer.tsx
export const CheckersRenderer: React.FC<Props> = ({ state, onMove }) => {
    // Render checkers board and handle moves
}
```

**Total impact on existing code:** Zero.

See [ADDING_GAMES.md](./docs/ADDING_GAMES.md) for detailed walkthrough.

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
pytest tests/test_games.py -v  # Game-specific tests
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📈 Performance & Scaling

### Database Indexes
Pre-created for optimal leaderboard queries:
```javascript
db.scores.createIndex({ game_id: 1, score_value: -1 });
db.game_sessions.createIndex({ user_id: 1, status: 1 });
```

### Potential Optimizations
- Leaderboard caching (Redis)
- Message queues for score processing (Celery)
- CDN for game assets
- WebSocket for real-time multiplayer
- Async game state snapshots

## 🎯 Future Features

- [ ] Multiplayer games (Chess, Checkers vs friends)
- [ ] AI opponents (configurable difficulty)
- [ ] Achievements & badges
- [ ] In-game cosmetics
- [ ] Game tournaments
- [ ] Replay system
- [ ] Analytics dashboard
- [ ] Chat & social features
- [ ] Mobile apps

## 📝 Development Workflow

### For Backend Developers
1. Create game adapter implementing `GameAdapter` interface
2. Register in `GameRegistry`
3. Add tests in `tests/test_<game>.py`
4. Document game-specific scoring in docstrings
5. No need to touch existing game code

### For Frontend Developers
1. Create game renderer in `src/games/<game>/`
2. Add to `GameRenderer.tsx` routing
3. Test with API responses
4. Can work independently of backend developers

### For DevOps
Dockerfile and docker-compose.prod.yml provided. Standard FastAPI + MongoDB + React deployment.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-game`)
3. Follow architecture patterns in [SCALABLE_ARCHITECTURE.md](./docs/SCALABLE_ARCHITECTURE.md)
4. Add tests and documentation
5. Submit pull request

## 📄 License

MIT

## 📧 Support

For questions about architecture, see [SCALABLE_ARCHITECTURE.md](./docs/SCALABLE_ARCHITECTURE.md)
For questions about adding games, see [ADDING_GAMES.md](./docs/ADDING_GAMES.md)
For questions about frontend, see [FRONTEND_INTEGRATION.md](./docs/FRONTEND_INTEGRATION.md)

3. **For Local Development (Optional):**
   
   **Backend Setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cd ..
   ```

   **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### Running the Application

#### Option 1: Using Dev Containers (Recommended)
This is the easiest development experience with automatic setup:

1. **Before opening the project**, ensure Docker Desktop is running on your Mac. You can run this helper script to verify:
   ```bash
   bash scripts/ensure-docker-local.sh
   ```

2. Open the project in VS Code.
3. VS Code will detect the `.devcontainer/devcontainer.json` and prompt you to "Reopen in Container" — click it.
4. Wait for the container to build and dependencies to install (first time only, a few minutes).
5. Once ready, VS Code opens inside the container with everything pre-configured.

6. **Configure VS Code Settings (First Time Only)**
   Copy the settings template to create your local configuration:
   ```bash
   cp .vscode/settings.example.json .vscode/settings.json
   ```
   This enables test discovery for both backend (pytest) and frontend (vitest) in the Testing tab.

All dependencies are automatically installed! Start the dev servers using the **Run and Debug** tab in VS Code:

1. Open the **Run and Debug** view (Ctrl+Shift+D / Cmd+Shift+D)
2. Select **"Full Stack"** from the dropdown to run both backend and frontend
3. Or run them individually:
   - **"Backend (Uvicorn)"** — Python debug server on port 5001
   - **"Frontend (Vite Dev)"** — Vite dev server on port 5173

You can also run them manually in terminals if preferred:

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 5001
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Access the application:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:5001`
- MongoDB: Runs automatically in the container

Code changes trigger instant hot-reload. Only rebuild the container if you change `requirements.txt` or `package.json`.

#### Option 2: Using Docker Compose (Production-like)
For testing the full containerized stack:
```bash
docker-compose -f docker-compose.prod.yml up
```

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:5001`

#### Option 3: Running Locally Without Docker

Start MongoDB separately, then:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 5001
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### License
This project is licensed under the MIT License.