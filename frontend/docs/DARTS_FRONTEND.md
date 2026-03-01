# Darts Frontend Implementation

## Overview

The Darts game frontend provides a complete UI for playing darts with score tracking. Users configure players, throw darts (by selecting dart values), and see live updates of scores and game progress.

## Components

### 1. **DartsBoard** (`src/components/DartsBoard.tsx`)
The main game interface component.

**Features:**
- ✅ Displays all players and their current scores
- ✅ Highlights the active player
- ✅ Shows player's current score in large text
- ✅ Dart progress indicator (1 of 3, 2 of 3, 3 of 3)
- ✅ Shows darts thrown in current turn
- ✅ Interactive dartboard with:
  - Numbers 1-20 (single, double, triple buttons)
  - Outer bullseye (25)
  - Inner bullseye (50)
  - Miss (0)
- ✅ Color-coded buttons:
  - **Singles**: Blue
  - **Doubles**: Yellow/Gold
  - **Triples**: Red
  - **25**: Orange
  - **50**: Red (bullseye)
  - **Miss**: Gray
- ✅ Turn history showing previous turns with scores
- ✅ Bust detection and display
- ✅ Winner announcement when game ends

**Props:**
```typescript
interface DartsBoardProps {
  gameState: {
    players: Array<{ user_id: string; score: number; status: string }>;
    current_player_index: number;
    turn_darts: number[];
    turn_start_score: number;
    history: Array<TurnHistory>;
    game_status: string;
    winner_user_id?: string;
  };
  sessionId: string;
  userId: string;
  onMove: (dartScore: number, isFinal: boolean) => Promise<void>;
  isLoading?: boolean;
}
```

### 2. **DartsGame** Page (`src/pages/DartsGame.tsx`)
The main game play page.

**Features:**
- Fetches game state from backend
- Polls for updates every 500ms
- Submits dart moves to API
- Automatically navigates to results when game ends
- Error handling and loading states

**Route:**
```
/games/darts/play/:sessionId
```

### 3. **DartsSetup** Page (`src/pages/DartsSetup.tsx`)
Game configuration page.

**Features:**
- ✅ Add/remove players (2-8 players)
- ✅ Edit player names
- ✅ Display game rules
- ✅ Create new game session
- ✅ Validation (minimum 2 players)

**Route:**
```
/games/darts/start
```

### 4. **DartsResults** Page (`src/pages/DartsResults.tsx`)
Game results/victory screen.

**Features:**
- ✅ Display final scores
- ✅ Show winner with trophy icon
- ✅ Rank placement (🥇🥈🥉)
- ✅ Navigation back to games or to new game

**Route:**
```
/games/darts/results/:sessionId
```

## Styling

### CSS File: `src/styles/DartsBoard.css`

The CSS provides:
- **Responsive grid layout** for dartboard (auto-fit columns)
- **Color-coded dart buttons** by type (single, double, triple)
- **Dark gradient background** (purple gradient)
- **Player scoreboard** with active player highlight
- **Dart progress indicator** with visual feedback
- **Mobile-responsive design**
- **Animations** for button clicks and state changes

#### Key Classes:
```css
.dart-btn.single       /* Blue buttons for singles 1-20 */
.dart-btn.double       /* Yellow buttons for doubles 2-40 */
.dart-btn.triple       /* Red buttons for triples 3-60 */
.dart-btn.outer-bull   /* Orange button for 25 */
.dart-btn.bull         /* Red button for 50 */
.dart-btn.miss         /* Gray button for 0 */
.dart-indicator.active /* Highlights current dart to throw */
.player-card.active    /* Purple gradient for active player */
```

## Game Flow

```
DartsSetup (Configure Players)
    ↓
[POST /api/games/darts/start] → Creates game session
    ↓
DartsGame (Play)
    ← [GET /api/games/darts/sessions/:id] (Poll every 500ms)
    ← [POST /api/games/darts/sessions/:id/move] (Submit dart)
    ↓
Game Complete → Auto-navigate to Results
    ↓
DartsResults (Show Winner & Scores)
    ↓
[Play Again] → Back to Setup
```

## API Integration

### Start Game
```typescript
POST /api/games/darts/start
{
  user_id: string;
  players: string[];
  difficulty?: string;
}
Response: { session_id: string; game_state: GameState }
```

### Get Game State
```typescript
GET /api/games/darts/sessions/:sessionId
Response: { game_state: GameState }
```

### Submit Dart
```typescript
POST /api/games/darts/sessions/:sessionId/move
{
  dart_score: number;
  is_final: boolean;
}
Response: {
  game_state: GameState;
  message: string;
}
```

## Routing Setup

Add these routes to your `App.tsx`:

```typescript
import DartsSetup from './pages/DartsSetup';
import DartsGame from './pages/DartsGame';
import DartsResults from './pages/DartsResults';

<Routes>
  {/* ... existing routes ... */}
  <Route path="/games/darts/start" element={<DartsSetup />} />
  <Route path="/games/darts/play/:sessionId" element={<DartsGame />} />
  <Route path="/games/darts/results/:sessionId" element={<DartsResults />} />
</Routes>
```

## Usage Example

### Basic Integration

```typescript
// In GameList or similar discovery component
<button onClick={() => navigate('/games/darts/start')}>
  Play Darts
</button>
```

### Advanced: Custom Renderer

```typescript
import DartsBoard from '../components/DartsBoard';
import { useGameState } from '../hooks/useGameState';

function CustomDartsRenderer() {
  const { gameState, submitMove } = useGameState('darts', sessionId);
  
  return (
    <DartsBoard
      gameState={gameState}
      sessionId={sessionId}
      userId={userId}
      onMove={submitMove}
    />
  );
}
```

## Features Explained

### Dart Progress Indicator
Shows which of the 3 darts in the current turn:
- **Gray circle**: Not thrown yet
- **Blue circle** (active): This dart is about to be thrown
- **Purple circle** (thrown): Already thrown

### Player Scoreboard
- **Active player** highlighted with gradient background and scale effect
- **Finished status** indicated with ✓ checkmark
- **Bust status** shown with red background
- **Large score display** for tracking

### Dartboard Grid
- **Organized by numbers** (1-20) in columns
- **Three buttons per number**: Single, Double, Triple
- **Color-coded** for quick visual recognition
- **Mobile-responsive**: Wraps to fewer columns on small screens

### Turn History
- **Scrollable list** of previous turns
- **Shows**: Player name, darts thrown, score change
- **Highlights busts** with different styling
- **Most recent turn** at the top

## Mobile Responsiveness

The UI is fully responsive:
- **Desktop**: Full dartboard grid (20 columns)
- **Tablet**: 2-3 mini columns with wrapping
- **Mobile**: Stacked layout with optimized touch targets

Touch areas (buttons) are at least 44x44px for easy interaction on mobile devices.

## Accessibility Features

- ✅ Button `title` attributes for dart value descriptions
- ✅ Color + text for important states (doubles, triples, bullseye)
- ✅ Large text for current score and player names
- ✅ High contrast mode-friendly colors
- ✅ Semantic HTML with proper headings

## Known Limitations & Future Improvements

### Current Limitations:
1. Game state polling (500ms) instead of WebSocket
2. No undo/correction for mistyped dart
3. No multi-player real-time UI updates
4. Results page shows basic ranking (could be more detailed)

### Future Enhancements:
1. WebSocket for real-time updates (lower latency)
2. Analytics dashboard (average score, best dart, etc.)
3. Game history and statistics
4. Elo rating or leaderboard integration
5. Statistics tracking (180s hit, perfect rounds, etc.)
6. Custom dartboard themes
7. Sound effects for scoring
8. Voice input for dart scores (accessibility)

## Testing

### Test Game Flow:
1. Navigate to `/games/darts/start`
2. Add 2-4 test players
3. Click "Start Game"
4. Take turns selecting dart values
5. Watch scores update in real-time
6. Continue until someone reaches 0
7. Verify winner screen shows correctly

### Test Edge Cases:
- Bust (go below 0): Score should revert
- Double out requirement: Final dart must be double/50
- Multiple players: Verify turn rotation
- Game completion: Auto-navigate to results

## Code Organization

```
frontend/src/
├── components/
│   ├── DartsBoard.tsx          ← Main game UI
│   └── ... (other components)
├── pages/
│   ├── DartsSetup.tsx          ← Game setup
│   ├── DartsGame.tsx           ← Game play
│   ├── DartsResults.tsx        ← Results
│   └── ... (other pages)
├── styles/
│   ├── DartsBoard.css          ← Game styling
│   └── ... (other styles)
└── ... (other files)
```

## Customization

### Change Colors:
Edit `DartsBoard.css` and update gradient colors:
```css
.darts-board {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  /* Change these hex values */
}
```

### Change Button Layout:
Modify `dart-grid` grid-template-columns in `DartsBoard.css`:
```css
.dart-grid {
  grid-template-columns: repeat(15, 1fr); /* Change from auto-fit minmax */
}
```

### Add Sound Effects:
In `DartsGame.tsx`, add after successful move:
```typescript
new Audio('/sounds/dart-throw.mp3').play();
```

### Custom Scorer:
Extend `DartsBoard` component to add custom scoring logic.
