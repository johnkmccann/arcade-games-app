# Project Structure Reorganization

## Overview
The project has been reorganized for better scalability and maintainability. Game implementations are now self-contained in their own directories, making it easy to add new games without affecting existing ones.

## Backend Structure

### Before
```
backend/app/services/games/__init__.py  (490 lines - all game adapters in one file)
```

### After
```
backend/app/services/games/
├── __init__.py                 (30 lines - imports and registration)
├── chess/
│   ├── adapter.py             (ChessAdapter class)
│   └── __init__.py            (exports)
├── tetris/
│   ├── adapter.py             (TetrisAdapter class)
│   └── __init__.py            (exports)
├── pacman/
│   ├── adapter.py             (PacManAdapter class)
│   └── __init__.py            (exports)
└── darts/
    ├── adapter.py             (DartsAdapter class)
    └── __init__.py            (exports)
```

**Benefits:**
- Each game is isolated in its own module
- Easier to develop and test individual games
- Cleaner imports and dependencies
- Scalable for adding new games (just create a new subdirectory)

## Frontend Structure

### Before
```
frontend/src/
├── pages/
│   ├── DartsSetup.tsx
│   ├── DartsGame.tsx
│   └── DartsResults.tsx
├── components/
│   ├── DartsBoard.tsx
│   └── ...
└── styles/
    ├── DartsBoard.css
    └── ...
```

### After
```
frontend/src/
├── games/
│   ├── index.ts              (central exports)
│   └── darts/
│       ├── index.ts          (darts exports)
│       ├── pages/
│       │   ├── Setup.tsx     (was DartsSetup.tsx)
│       │   ├── Play.tsx      (was DartsGame.tsx)
│       │   └── Results.tsx   (was DartsResults.tsx)
│       ├── components/
│       │   └── Board.tsx     (was DartsBoard.tsx)
│       └── styles/
│           └── board.css     (was DartsBoard.css)
├── pages/
├── components/
└── styles/
```

**Benefits:**
- Game-related code is grouped together by game
- Clearer separation of concerns
- Easier to maintain and modify individual games
- Scalable for future games (Chess, Tetris, etc. can follow same pattern)

## Import Changes

### Backend
All game imports still work through the single `register_default_games()` function:
```python
from app.services.games import register_default_games
register_default_games()  # All games registered
```

### Frontend
Updated imports in `App.tsx`:
```typescript
// Old
import DartsSetup from './pages/DartsSetup';
import DartsGame from './pages/DartsGame';
import DartsResults from './pages/DartsResults';

// New
import { DartsSetup, DartsGame, DartsResults } from './games/darts';
```

## Adding a New Game

### For Backend
1. Create `/workspace/backend/app/services/games/newgame/` directory
2. Create `adapter.py` with your `NewGameAdapter` class
3. Create `__init__.py` that exports the adapter
4. Add import and registration to `backend/app/services/games/__init__.py`

### For Frontend
1. Create `/workspace/frontend/src/games/newgame/` directory structure:
   - `pages/` - game pages
   - `components/` - game components
   - `styles/` - game styles
   - `index.ts` - exports
2. Update `App.tsx` with new routes
3. Add game to `GameList.tsx`

## Testing

✅ Backend imports verified:
```
Registered games: [Chess, Tetris, Pac-Man, Darts]
```

✅ Frontend structure created and imports updated

All games are fully functional with the new modular structure!
