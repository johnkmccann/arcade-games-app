import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Board from '../components/Board';

interface GameState {
  players: Array<{
    user_id: string;
    score: number;
    status: 'active' | 'finished' | 'busted';
    busted?: boolean;
  }>;
  current_player_index: number;
  turn_darts: number[];
  turn_start_score: number;
  history: Array<{
    player_index: number;
    darts: number[];
    start_score: number;
    end_score: number;
    busted: boolean;
  }>;
  game_status: string;
  winner_user_id?: string;
}

const DartsGame: React.FC = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [userId] = useState<string>(localStorage.getItem('userId') || 'guest');

  // Fetch current game state
  const fetchGameState = async () => {
    if (!sessionId) return;

    try {
      const response = await fetch(
        `/api/games/darts/sessions/${sessionId}`
      );
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(errorData.detail || `HTTP ${response.status}`);
      }

      const data = await response.json();
      setGameState(data.game_state || data);
      setError(null);
    } catch (e) {
      setError((e as Error).message);
      console.error('Error fetching game state:', e);
    }
  };

  // Initial load
  useEffect(() => {
    fetchGameState();
  }, [sessionId]);

  // Poll for updates every 500ms
  useEffect(() => {
    const interval = setInterval(() => {
      fetchGameState();
    }, 500);

    return () => clearInterval(interval);
  }, [sessionId]);

  // Handle dart submission
  const handleDartMove = async (dartScore: number, isFinal: boolean) => {
    if (!sessionId) return;

    setIsLoading(true);
    try {
      const response = await fetch(
        `/api/games/darts/sessions/${sessionId}/move`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            dart_score: dartScore,
            is_final: isFinal,
          }),
        }
      );

      if (!response.ok) throw new Error('Failed to submit dart');

      const data = await response.json();
      setGameState(data.game_state);

      // If game finished, wait a moment then go to results
      if (data.game_state.game_status === 'finished') {
        setTimeout(() => {
          navigate(`/games/darts/results/${sessionId}`);
        }, 2000);
      }
    } catch (e) {
      setError((e as Error).message);
      console.error('Error submitting dart:', e);
    } finally {
      setIsLoading(false);
    }
  };

  if (error) {
    return (
      <div className="error-container">
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={() => navigate('/games')}>Back to Games</button>
      </div>
    );
  }

  if (!gameState) {
    return (
      <div className="loading-container">
        <h2>Loading game...</h2>
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="darts-game-page">
      <Board
        gameState={gameState}
        sessionId={sessionId || ''}
        userId={userId}
        onMove={handleDartMove}
        isLoading={isLoading}
      />
    </div>
  );
};

export default DartsGame;
