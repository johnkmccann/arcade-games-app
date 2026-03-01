# Frontend Integration Guide

## Architecture Overview

The frontend needs to be **game-agnostic** - it discovers games dynamically and renders them generically.

```
┌─────────────────────────────────────┐
│         React Application            │
├─────────────────────────────────────┤
│  GameDiscovery         GameLobby      │
│  GameCanvas (generic)   Leaderboard   │
│  ScoreBoard            UserProfile    │
├─────────────────────────────────────┤
│    GameAdapter (browser)             │
│  (converts game_state to UI)         │
├─────────────────────────────────────┤
│    API Client                        │
├─────────────────────────────────────┤
│  Backend /games, /leaderboard, etc  │
└─────────────────────────────────────┘
```

## Key Components

### 1. Game Discovery UI

```typescript
// src/pages/GameLibrary.tsx

import React, { useEffect, useState } from 'react';
import { GameCard } from '../components/GameCard';
import api from '../services/api';
import { GameMetadata } from '../types';

export const GameLibrary: React.FC = () => {
  const [games, setGames] = useState<GameMetadata[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>('all'); // 'arcade', 'boardgame', 'puzzle'

  useEffect(() => {
    const fetchGames = async () => {
      try {
        const response = await api.get('/games', {
          params: { user_id: currentUserId }
        });
        setGames(response.data);
      } catch (error) {
        console.error('Failed to fetch games:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchGames();
  }, []);

  const filteredGames = filter === 'all' 
    ? games 
    : games.filter(g => g.game_type === filter);

  return (
    <div className="game-library">
      <h1>Arcade Games</h1>
      
      <div className="filters">
        <button onClick={() => setFilter('all')}>All</button>
        <button onClick={() => setFilter('arcade')}>Arcade</button>
        <button onClick={() => setFilter('boardgame')}>Board Games</button>
        <button onClick={() => setFilter('puzzle')}>Puzzles</button>
      </div>

      <div className="game-grid">
        {filteredGames.map(game => (
          <GameCard key={game.id} game={game} />
        ))}
      </div>
    </div>
  );
};
```

### 2. Game Card Component

```typescript
// src/components/GameCard.tsx

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { GameMetadata } from '../types';

interface Props {
  game: GameMetadata;
}

export const GameCard: React.FC<Props> = ({ game }) => {
  const [isStarting, setIsStarting] = useState(false);

  const handleStartGame = async (difficulty?: string) => {
    setIsStarting(true);
    try {
      const response = await api.post(`/games/${game.id}/start`, {
        user_id: currentUserId,
        difficulty
      });
      
      const sessionId = response.data.id;
      window.location.href = `/play/${game.id}/${sessionId}`;
    } catch (error) {
      console.error('Failed to start game:', error);
      setIsStarting(false);
    }
  };

  return (
    <div className="game-card">
      <img 
        src={game.thumbnail_url || `/images/games/${game.id}.png`}
        alt={game.title}
      />
      
      <h3>{game.title}</h3>
      <p className="genre">{game.genre}</p>
      <p className="description">{game.description}</p>
      
      <div className="stats">
        <span>⭐ {game.rating?.toFixed(1)} / 10</span>
        <span>👥 {game.min_players}-{game.max_players} players</span>
        <span>⏱️ {game.avg_playtime_minutes} min</span>
      </div>
      
      <div className="actions">
        <button 
          onClick={() => handleStartGame()}
          disabled={isStarting}
          className="btn-primary"
        >
          {isStarting ? 'Starting...' : 'Play'}
        </button>
        
        {/* Difficulty selector for games with multiple difficulties */}
        <div className="difficulty-menu">
          <button onClick={() => handleStartGame('easy')}>Easy</button>
          <button onClick={() => handleStartGame('normal')}>Normal</button>
          <button onClick={() => handleStartGame('hard')}>Hard</button>
        </div>
        
        <Link to={`/game/${game.id}`} className="btn-secondary">
          Details
        </Link>
      </div>
    </div>
  );
};
```

### 3. Generic Game Canvas Component

The key insight: **don't hardcode chess, tetris, etc.** Pass the game_state to a dynamic renderer.

```typescript
// src/components/GameCanvas.tsx

import React, { useState, useEffect } from 'react';
import { GameSession, GameMetadata } from '../types';
import api from '../services/api';

interface Props {
  gameId: string;
  sessionId: string;
}

export const GameCanvas: React.FC<Props> = ({ gameId, sessionId }) => {
  const [session, setSession] = useState<GameSession | null>(null);
  const [metadata, setMetadata] = useState<GameMetadata | null>(null);
  const [loading, setLoading] = useState(true);
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState<string | null>(null);

  useEffect(() => {
    const fetchGame = async () => {
      try {
        const [sessionResponse, metadataResponse] = await Promise.all([
          api.get(`/games/${gameId}/sessions/${sessionId}`),
          api.get(`/games/${gameId}`)
        ]);
        
        setSession(sessionResponse.data);
        setMetadata(metadataResponse.data);
      } catch (error) {
        console.error('Failed to fetch game:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchGame();
  }, [gameId, sessionId]);

  const handleMove = async (move: any) => {
    if (!session) return;

    try {
      const response = await api.post(
        `/games/${gameId}/sessions/${sessionId}/move`,
        move
      );

      const { session: updatedSession, is_game_over, winner: newWinner } = response.data;
      
      setSession(updatedSession);
      
      if (is_game_over) {
        setGameOver(true);
        setWinner(newWinner);
        
        // Save final score
        await api.post(`/games/${gameId}/sessions/${sessionId}/finish`);
      }
    } catch (error) {
      console.error('Failed to make move:', error);
    }
  };

  if (loading) return <div>Loading game...</div>;
  if (!session || !metadata) return <div>Game not found</div>;

  return (
    <div className="game-canvas">
      <div className="game-header">
        <h1>{metadata.title}</h1>
        <div className="game-info">
          <span>Score: {session.score || 'N/A'}</span>
          {session.score_breakdown && (
            <details>
              <summary>Score Breakdown</summary>
              <pre>{JSON.stringify(session.score_breakdown, null, 2)}</pre>
            </details>
          )}
        </div>
      </div>

      {gameOver ? (
        <GameOverScreen 
          winner={winner}
          score={session.score}
          scoreBreakdown={session.score_breakdown}
          onPlayAgain={() => window.location.href = `/games/${gameId}`}
        />
      ) : (
        <>
          {/* Render game-specific UI based on metadata */}
          <GameRenderer 
            gameId={gameId}
            gameState={session.game_state}
            metadata={metadata}
            onMove={handleMove}
          />
          
          <div className="game-controls">
            <button onClick={() => window.location.href = `/games`}>
              Exit Game
            </button>
            <button onClick={() => api.post(`/games/${gameId}/sessions/${sessionId}/finish`)}>
              Save & Exit
            </button>
          </div>
        </>
      )}
    </div>
  );
};
```

### 4. Game Renderer (Dynamic Game-Specific UI)

This is where each game defines how its `game_state` is rendered and controlled.

```typescript
// src/components/GameRenderer.tsx

import React from 'react';
import { ChessRenderer } from '../games/chess/ChessRenderer';
import { TetrisRenderer } from '../games/tetris/TetrisRenderer';
import { PacManRenderer } from '../games/pacman/PacManRenderer';
import { GameMetadata } from '../types';

interface Props {
  gameId: string;
  gameState: any;
  metadata: GameMetadata;
  onMove: (move: any) => Promise<void>;
}

export const GameRenderer: React.FC<Props> = ({
  gameId,
  gameState,
  metadata,
  onMove
}) => {
  // Route to game-specific renderer
  switch (gameId) {
    case 'chess':
      return <ChessRenderer state={gameState} onMove={onMove} />;
    
    case 'tetris':
      return <TetrisRenderer state={gameState} onMove={onMove} />;
    
    case 'pacman':
      return <PacManRenderer state={gameState} onMove={onMove} />;
    
    default:
      return (
        <div className="generic-game-renderer">
          <h3>Game State (JSON)</h3>
          <pre>{JSON.stringify(gameState, null, 2)}</pre>
          <p>TODO: Implement renderer for {gameId}</p>
        </div>
      );
  }
};
```

### 5. Chess Renderer Example

```typescript
// src/games/chess/ChessRenderer.tsx

import React, { useState } from 'react';
import { ChessBoard } from './ChessBoard';
import { MovesPanel } from './MovesPanel';

interface Props {
  state: any; // Chess game_state
  onMove: (move: any) => Promise<void>;
}

export const ChessRenderer: React.FC<Props> = ({ state, onMove }) => {
  const [selectedSquare, setSelectedSquare] = useState<string | null>(null);
  const [legalMoves, setLegalMoves] = useState<string[]>([]);

  const handleSquareClick = async (square: string) => {
    if (!selectedSquare) {
      // First click - select a piece
      setSelectedSquare(square);
      // Calculate legal moves for this square
      // This could come from backend via getLegalMoves() API call
      const moves = getChessLegalMoves(state.fen, square);
      setLegalMoves(moves);
    } else {
      // Second click - make the move
      await onMove({
        from: selectedSquare,
        to: square
      });
      setSelectedSquare(null);
      setLegalMoves([]);
    }
  };

  return (
    <div className="chess-game">
      <ChessBoard 
        fen={state.fen}
        selectedSquare={selectedSquare}
        legalMoves={legalMoves}
        onSquareClick={handleSquareClick}
      />
      
      <MovesPanel moves={state.moves} />
      
      <div className="game-info">
        <p>Current player: {state.current_player === 'white' ? '♔' : '♚'}</p>
      </div>
    </div>
  );
};

function getChessLegalMoves(fen: string, square: string): string[] {
  // Use chess.js library or similar
  // returns ['a4', 'a3', etc]
  return [];
}
```

### 6. Leaderboard Component

```typescript
// src/components/Leaderboard.tsx

import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { ScoreLeaderboard } from '../types';

interface Props {
  gameId: string;
  timePeriod?: 'all_time' | 'weekly' | 'daily';
}

export const Leaderboard: React.FC<Props> = ({ gameId, timePeriod = 'all_time' }) => {
  const [leaderboard, setLeaderboard] = useState<ScoreLeaderboard[]>([]);
  const [loading, setLoading] = useState(true);
  const [displayType, setDisplayType] = useState<'global' | 'friends'>('global');

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const endpoint = displayType === 'friends'
          ? `/games/${gameId}/leaderboard/friends?user_id=${currentUserId}`
          : `/games/${gameId}/leaderboard?time_period=${timePeriod}`;
        
        const response = await api.get(endpoint);
        setLeaderboard(response.data.leaderboard);
      } catch (error) {
        console.error('Failed to fetch leaderboard:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, [gameId, timePeriod, displayType]);

  if (loading) return <div>Loading leaderboard...</div>;

  return (
    <div className="leaderboard">
      <div className="leaderboard-header">
        <h2>Leaderboard</h2>
        
        <div className="controls">
          <button 
            onClick={() => setDisplayType('global')}
            className={displayType === 'global' ? 'active' : ''}
          >
            Global
          </button>
          <button 
            onClick={() => setDisplayType('friends')}
            className={displayType === 'friends' ? 'active' : ''}
          >
            Friends
          </button>
        </div>
      </div>

      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Player</th>
            <th>Score</th>
            <th>Time</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {leaderboard.map((entry, index) => (
            <tr key={entry.user_id} className={entry.user_id === currentUserId ? 'highlight' : ''}>
              <td className="rank">#{entry.rank}</td>
              <td className="player">
                {entry.user_id === currentUserId ? '⭐ ' : ''}
                {entry.username}
              </td>
              <td className="score">{entry.score_value}</td>
              <td className="time">
                {entry.play_duration_seconds 
                  ? `${Math.floor(entry.play_duration_seconds / 60)}m`
                  : '-'
                }
              </td>
              <td className="date">
                {new Date(entry.achieved_at).toLocaleDateString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
```

### 7. User Profile - Games & Progress

```typescript
// src/pages/UserProfile.tsx

import React, { useEffect, useState } from 'react';
import api from '../services/api';

interface GameProgress {
  gameId: string;
  gameTitle: string;
  bestScore: number;
  totalPlays: number;
  rank: number;
  lastPlayed: string;
}

interface Props {
  userId: string;
}

export const UserProfile: React.FC<Props> = ({ userId }) => {
  const [gameProgress, setGameProgress] = useState<GameProgress[]>([]);
  const [favorites, setFavorites] = useState<string[]>([]);
  const [unfinished, setUnfinished] = useState<any[]>([]);

  useEffect(() => {
    const fetchUserProgress = async () => {
      try {
        // Get all available games
        const gamesResponse = await api.get('/games');
        const games = gamesResponse.data;

        // Get stats for each game
        const statsPromises = games.map(game => 
          api.get(`/games/${game.id}/user/${userId}/stats`)
            .catch(() => null)
        );
        
        const allStats = await Promise.all(statsPromises);
        const progress = allStats
          .filter(s => s !== null)
          .map((s, i) => ({
            gameId: games[i].id,
            gameTitle: games[i].title,
            bestScore: s.data.best_score,
            totalPlays: s.data.total_plays,
            rank: s.data.rank,
            lastPlayed: s.data.last_played
          }));
        
        setGameProgress(progress.filter(p => p.totalPlays > 0)); // Only games played
      } catch (error) {
        console.error('Failed to fetch game stats:', error);
      }
    };

    fetchUserProgress();
  }, [userId]);

  return (
    <div className="user-profile">
      <h1>My Games</h1>

      <section className="favorites">
        <h2>Favorite Games</h2>
        <div className="game-list">
          {favorites.map(gameId => (
            <div key={gameId} className="game-item">
              {gameId} ⭐
            </div>
          ))}
        </div>
      </section>

      <section className="game-progress">
        <h2>My Progress</h2>
        <table>
          <thead>
            <tr>
              <th>Game</th>
              <th>Best Score</th>
              <th>Times Played</th>
              <th>Rank</th>
              <th>Last Played</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {gameProgress.map(game => (
              <tr key={game.gameId}>
                <td>{game.gameTitle}</td>
                <td>{game.bestScore}</td>
                <td>{game.totalPlays}</td>
                <td>#{game.rank}</td>
                <td>{new Date(game.lastPlayed).toLocaleDateString()}</td>
                <td>
                  <a href={`/play/${game.gameId}`}>Play Again</a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="unfinished">
        <h2>Unfinished Games</h2>
        {unfinished.length === 0 ? (
          <p>No unfinished games</p>
        ) : (
          <div className="game-list">
            {unfinished.map(session => (
              <div key={session.id} className="unfinished-game">
                <h4>{session.gameId}</h4>
                <p>Started {new Date(session.started_at).toLocaleDateString()}</p>
                <a href={`/play/${session.game_id}/${session.id}`}>Resume</a>
                <button onClick={() => api.post(`/games/${session.game_id}/sessions/${session.id}/finish`)}>
                  Finish & Save
                </button>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
};
```

## Type Definitions

```typescript
// src/types/index.ts

export interface GameMetadata {
  id: string;
  title: string;
  genre: string;
  description?: string;
  developer?: string;
  game_type: 'arcade' | 'boardgame' | 'puzzle';
  min_players: number;
  max_players: number;
  avg_playtime_minutes?: number;
  scoring_type: string;
  scoring_direction: 'higher_better' | 'lower_better';
  max_score?: number;
  rating?: number;
  thumbnail_url?: string;
  created_at: string;
  updated_at: string;
}

export interface GameSession {
  id: string;
  user_id: string;
  game_id: string;
  status: 'in_progress' | 'completed' | 'abandoned';
  game_state: Record<string, any>;
  score?: number;
  score_breakdown?: Record<string, any>;
  started_at: string;
  completed_at?: string;
}

export interface ScoreLeaderboard {
  rank: number;
  user_id: string;
  username: string;
  score_value: number;
  achieved_at: string;
  play_duration_seconds?: number;
}
```

## State Management (Zustand recommended)

```typescript
// src/store/gameStore.ts

import create from 'zustand';
import { GameSession } from '../types';

interface GameState {
  currentSession: GameSession | null;
  setCurrentSession: (session: GameSession | null) => void;
  updateGameState: (newState: any) => void;
}

export const useGameStore = create<GameState>(set => ({
  currentSession: null,
  
  setCurrentSession: (session) => set({ currentSession: session }),
  
  updateGameState: (newState) => set(state => ({
    currentSession: state.currentSession
      ? { ...state.currentSession, game_state: newState }
      : null
  }))
}));
```

## Summary

Key frontend principles:

1. **Game discovery is dynamic** - fetch from `/games` endpoint
2. **Game state is generic** - renderer switches based on `gameId`
3. **No hardcoded game logic** - all state comes from backend
4. **Type-safe** - use TypeScript for game state interface
5. **Leaderboards are data-driven** - fetch scores from API
6. **Extensible** - adding new game means adding one renderer component

This approach means the frontend scales automatically as new games are added to the backend.
