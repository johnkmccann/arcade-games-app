import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

interface ScoreData {
  user_id: string;
  score: number;
  final_score: number;
  rank: number;
}

const DartsResults: React.FC = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const [scores, setScores] = useState<ScoreData[]>([]);
  const [winner, setWinner] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchResults = async () => {
      if (!sessionId) return;

      try {
        // Fetch the finished game session to get final state
        const sessionResponse = await fetch(
          `/api/games/darts/sessions/${sessionId}`
        );
        if (!sessionResponse.ok) throw new Error('Failed to fetch results');

        const sessionData = await sessionResponse.json();
        const gameState = sessionData.game_state;

        // Build scores from game state
        const playerScores = gameState.players.map(
          (player: any, index: number) => ({
            user_id: player.user_id,
            score: player.score,
            final_score: gameState.history
              .filter((turn: any) => turn.player_index === index)
              .reduce((acc: number, turn: any) => acc + 1, 0), // Count of turns
            rank: player.score === 0 ? 1 : 2, // Simple ranking by remaining score
          })
        );

        setScores(
          playerScores.sort((a: ScoreData, b: ScoreData) => a.score - b.score)
        );
        setWinner(gameState.winner_user_id || '');
        setError(null);
      } catch (e) {
        setError((e as Error).message);
        console.error('Error fetching results:', e);
      } finally {
        setIsLoading(false);
      }
    };

    fetchResults();
  }, [sessionId]);

  if (isLoading) {
    return (
      <div className="results-container loading">
        <h2>Loading results...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div className="results-container error">
        <h2>Error loading results</h2>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="darts-results">
      <div className="results-header">
        <h1>🎯 Game Over!</h1>
        <h2 className="winner">🏆 {winner} Wins!</h2>
      </div>

      <div className="final-scores">
        <h3>Final Scores</h3>
        <div className="scores-list">
          {scores.map((player, index) => (
            <div
              key={player.user_id}
              className={`score-card ${index === 0 ? 'winner' : ''}`}
            >
              <div className="rank">
                {index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉'}
              </div>
              <div className="player-info">
                <div className="player-name">{player.user_id}</div>
                <div className="final-value">
                  Ended at: {player.score}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="actions">
        <button className="btn btn-primary" onClick={() => navigate('/games')}>
          Back to Games
        </button>
        <button
          className="btn btn-secondary"
          onClick={() => navigate('/games/darts/start')}
        >
          Play Again
        </button>
      </div>

      <style>{`
        .darts-results {
          max-width: 600px;
          margin: 40px auto;
          padding: 20px;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .results-header {
          text-align: center;
          margin-bottom: 40px;
        }

        .results-header h1 {
          font-size: 40px;
          margin: 0 0 20px 0;
          color: #667eea;
        }

        .results-header .winner {
          font-size: 32px;
          margin: 0;
          color: #f57f17;
          text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }

        .final-scores {
          margin-bottom: 40px;
        }

        .final-scores h3 {
          font-size: 20px;
          margin-bottom: 20px;
          color: #333;
        }

        .scores-list {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .score-card {
          display: flex;
          align-items: center;
          gap: 16px;
          padding: 16px;
          background: #f5f5f5;
          border-radius: 8px;
          border-left: 4px solid #ddd;
        }

        .score-card.winner {
          background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
          border-left-color: #f57f17;
          color: white;
        }

        .score-card .rank {
          font-size: 28px;
          min-width: 40px;
        }

        .score-card .player-info {
          flex: 1;
        }

        .score-card .player-name {
          font-weight: 600;
          font-size: 18px;
          margin-bottom: 4px;
        }

        .score-card .final-value {
          font-size: 14px;
          opacity: 0.9;
        }

        .actions {
          display: flex;
          gap: 12px;
          justify-content: center;
        }

        .btn {
          padding: 12px 24px;
          border: none;
          border-radius: 6px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .btn-primary {
          background: #667eea;
          color: white;
        }

        .btn-primary:hover {
          background: #5568d3;
          transform: translateY(-2px);
        }

        .btn-secondary {
          background: #f57f17;
          color: white;
        }

        .btn-secondary:hover {
          background: #e65100;
          transform: translateY(-2px);
        }

        .results-container {
          text-align: center;
          padding: 40px 20px;
        }

        .results-container.loading h2 {
          color: #667eea;
        }

        .results-container.error {
          color: #c62828;
        }
      `}</style>
    </div>
  );
};

export default DartsResults;
