import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const DartsSetup: React.FC = () => {
  const navigate = useNavigate();
  const [playerNames, setPlayerNames] = useState<string[]>(['Player 1', 'Player 2']);
  const [newPlayerName, setNewPlayerName] = useState<string>('');
  const [isCreating, setIsCreating] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleAddPlayer = () => {
    if (newPlayerName.trim() && playerNames.length < 8) {
      setPlayerNames([...playerNames, newPlayerName]);
      setNewPlayerName('');
    }
  };

  const handleRemovePlayer = (index: number) => {
    if (playerNames.length > 2) {
      setPlayerNames(playerNames.filter((_, i) => i !== index));
    }
  };

  const handleUpdatePlayerName = (index: number, name: string) => {
    const updated = [...playerNames];
    updated[index] = name;
    setPlayerNames(updated);
  };

  const handleStartGame = async () => {
    if (playerNames.length < 2) {
      setError('At least 2 players are required');
      return;
    }

    setIsCreating(true);
    setError(null);
    try {
      // Create game session with first player
      const userId = localStorage.getItem('userId') || 'admin';
      const params = new URLSearchParams({
        user_id: userId,
        difficulty: 'normal',
      });

      console.log('Request details:', {
        url: `/api/games/darts/start?${params.toString()}`,
        method: 'POST',
        body: { players: playerNames }
      });

      const response = await fetch(`/api/games/darts/start?${params.toString()}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          players: playerNames,
        }),
      });

      console.log('Response status:', response.status);
      const data = await response.json();
      console.log('Response data:', data);
      console.log('Full response:', JSON.stringify(data, null, 2));

      if (!response.ok) {
        // Handle validation errors which come as an array
        if (Array.isArray(data.detail)) {
          const validationErrors = data.detail.map((err: any) => 
            `${err.loc?.join('.')}: ${err.msg}`
          ).join('; ');
          throw new Error(`Validation error: ${validationErrors}`);
        }
        throw new Error(data.detail || `Failed to create game (${response.status})`);
      }

      if (!data.id) {
        console.error('Response missing id field:', data);
        throw new Error('Server response missing session ID');
      }

      navigate(`/games/darts/play/${data.id}`);
    } catch (e) {
      const errorMsg = (e as Error).message;
      setError(errorMsg);
      console.error('Error creating game:', e);
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className="darts-setup">
      <div className="setup-container">
        <div className="setup-header">
          <h1>🎯 Darts Game Setup</h1>
          <p>Configure your players and start playing</p>
        </div>

        <div className="setup-content">
          <div className="players-section">
            <h2>Players</h2>
            <div className="players-list">
              {playerNames.map((name, index) => (
                <div key={index} className="player-input-group">
                  <span className="player-number">P{index + 1}</span>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => handleUpdatePlayerName(index, e.target.value)}
                    placeholder="Player name"
                    className="player-input"
                  />
                  {playerNames.length > 2 && (
                    <button
                      onClick={() => handleRemovePlayer(index)}
                      className="btn-remove"
                      title="Remove player"
                    >
                      ✕
                    </button>
                  )}
                </div>
              ))}
            </div>

            {playerNames.length < 8 && (
              <div className="add-player">
                <input
                  type="text"
                  value={newPlayerName}
                  onChange={(e) => setNewPlayerName(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleAddPlayer()}
                  placeholder="New player name"
                  className="player-input"
                />
                <button
                  onClick={handleAddPlayer}
                  className="btn-add"
                  disabled={!newPlayerName.trim()}
                >
                  Add Player
                </button>
              </div>
            )}

            {playerNames.length === 8 && (
              <p className="info-text">Maximum 8 players reached</p>
            )}
          </div>

          <div className="rules-section">
            <h2>Game Rules</h2>
            <ul className="rules-list">
              <li>Start with 501 points per player</li>
              <li>Players take turns throwing 3 darts</li>
              <li>Each dart score subtracts from your total</li>
              <li>Going below 0 = BUST (score unchanged)</li>
              <li>Final dart must be a double or bullseye</li>
              <li>First player to reach exactly 0 wins</li>
            </ul>
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="action-buttons">
            <button
              onClick={() => navigate('/games')}
              className="btn btn-cancel"
            >
              Cancel
            </button>
            <button
              onClick={handleStartGame}
              className="btn btn-start"
              disabled={playerNames.length < 2 || isCreating}
            >
              {isCreating ? 'Starting...' : 'Start Game'}
            </button>
          </div>
        </div>
      </div>

      <style>{`
        .darts-setup {
          min-height: 100vh;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          padding: 40px 20px;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .setup-container {
          max-width: 600px;
          margin: 0 auto;
        }

        .setup-header {
          text-align: center;
          color: white;
          margin-bottom: 40px;
        }

        .setup-header h1 {
          font-size: 36px;
          margin: 0 0 10px 0;
        }

        .setup-header p {
          font-size: 16px;
          opacity: 0.9;
          margin: 0;
        }

        .setup-content {
          background: white;
          border-radius: 12px;
          padding: 30px;
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }

        h2 {
          font-size: 20px;
          color: #333;
          margin-top: 0;
          margin-bottom: 16px;
          border-bottom: 2px solid #667eea;
          padding-bottom: 10px;
        }

        .players-list {
          display: flex;
          flex-direction: column;
          gap: 10px;
          margin-bottom: 20px;
        }

        .player-input-group {
          display: flex;
          gap: 10px;
          align-items: center;
        }

        .player-number {
          font-weight: 600;
          color: #667eea;
          min-width: 30px;
          text-align: center;
        }

        .player-input {
          flex: 1;
          padding: 10px 12px;
          border: 2px solid #ddd;
          border-radius: 6px;
          font-size: 14px;
          transition: all 0.3s ease;
        }

        .player-input:focus {
          outline: none;
          border-color: #667eea;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .btn-remove {
          width: 36px;
          height: 36px;
          border: 2px solid #ef5350;
          background: white;
          color: #ef5350;
          border-radius: 6px;
          cursor: pointer;
          font-weight: bold;
          transition: all 0.3s ease;
        }

        .btn-remove:hover {
          background: #ef5350;
          color: white;
        }

        .add-player {
          display: flex;
          gap: 10px;
          margin-bottom: 16px;
        }

        .btn-add {
          padding: 10px 20px;
          background: #667eea;
          color: white;
          border: none;
          border-radius: 6px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .btn-add:hover:not(:disabled) {
          background: #5568d3;
          transform: translateY(-2px);
        }

        .btn-add:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .info-text {
          font-size: 12px;
          color: #999;
          margin-top: 10px;
          margin-bottom: 0;
        }

        .rules-section {
          background: #f5f5f5;
          border-radius: 8px;
          padding: 16px;
          margin: 30px 0;
        }

        .rules-list {
          margin: 0;
          padding-left: 20px;
          color: #555;
        }

        .rules-list li {
          margin-bottom: 8px;
          line-height: 1.4;
        }

        .error-message {
          background: #ffebee;
          border-left: 4px solid #ef5350;
          padding: 12px;
          border-radius: 4px;
          color: #c62828;
          margin-bottom: 20px;
          font-size: 14px;
        }

        .action-buttons {
          display: flex;
          gap: 12px;
        }

        .btn {
          flex: 1;
          padding: 12px 20px;
          border: none;
          border-radius: 6px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .btn-cancel {
          background: #f5f5f5;
          color: #333;
          border: 2px solid #ddd;
        }

        .btn-cancel:hover {
          background: #e0e0e0;
        }

        .btn-start {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }

        .btn-start:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }

        .btn-start:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        @media (max-width: 480px) {
          .darts-setup {
            padding: 20px 15px;
          }

          .setup-content {
            padding: 20px;
          }

          .setup-header h1 {
            font-size: 28px;
          }

          .action-buttons {
            flex-direction: column;
          }

          .btn {
            width: 100%;
          }
        }
      `}</style>
    </div>
  );
};

export default DartsSetup;
