import React, { useState } from 'react';
import '../styles/DartsBoard.css';

interface Player {
  user_id: string;
  score: number;
  status: 'active' | 'finished' | 'busted';
  busted?: boolean;
}

interface DartsBoardProps {
  gameState: {
    players: Player[];
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
  };
  sessionId: string;
  userId: string;
  onMove: (dartScore: number, isFinal: boolean) => Promise<void>;
  isLoading?: boolean;
}

const DartsBoard: React.FC<DartsBoardProps> = ({
  gameState,
  sessionId,
  userId,
  onMove,
  isLoading = false,
}) => {
  const [selectedDart, setSelectedDart] = useState<number | null>(null);

  const currentPlayer = gameState.players[gameState.current_player_index];
  const currentScore = currentPlayer?.score ?? 0;
  const darts = [
    ...Array.from({ length: 20 }, (_, i) => ({
      value: i + 1,
      type: 'single' as const,
    })),
  ];

  const allDartOptions = [
    // Singles 1-20
    ...Array.from({ length: 20 }, (_, i) => ({
      label: String(i + 1),
      value: i + 1,
      category: 'single',
    })),
    // Doubles 2-40
    ...Array.from({ length: 20 }, (_, i) => ({
      label: `D${i + 1}`,
      value: (i + 1) * 2,
      category: 'double',
    })),
    // Triples 3-60
    ...Array.from({ length: 20 }, (_, i) => ({
      label: `T${i + 1}`,
      value: (i + 1) * 3,
      category: 'triple',
    })),
    // 25 and 50
    { label: '25', value: 25, category: 'outer_bull' },
    { label: '50', value: 50, category: 'bull' },
    // Miss
    { label: 'MISS', value: 0, category: 'miss' },
  ];

  const handleDartClick = async (dartScore: number) => {
    if (isLoading) return;

    setSelectedDart(dartScore);
    const dartsInTurn = gameState.turn_darts.length;
    const isFinal = dartsInTurn === 2; // This will be the 3rd dart

    try {
      await onMove(dartScore, isFinal);
      setSelectedDart(null);
    } catch (error) {
      console.error('Failed to submit dart:', error);
      setSelectedDart(null);
    }
  };

  const canPlayDarts = currentPlayer?.user_id === userId && gameState.game_status === 'active';

  return (
    <div className="darts-board">
      {/* Header - Active Player and Score */}
      <div className="darts-header">
        <div className="active-player-info">
          <h1>Darts Scorer</h1>
          {gameState.game_status === 'finished' ? (
            <div className="game-over">
              <h2>🎯 {gameState.winner_user_id} Wins!</h2>
            </div>
          ) : (
            <>
              <div className="current-player">
                <h2>{currentPlayer?.user_id || 'No Player'}</h2>
                <div className="current-score">{currentScore}</div>
              </div>
              <div className="dart-progress">
                <span className="label">Dart Progress:</span>
                <div className="dart-counter">
                  {[1, 2, 3].map((num) => (
                    <div
                      key={num}
                      className={`dart-indicator ${
                        gameState.turn_darts.length >= num
                          ? 'thrown'
                          : num === gameState.turn_darts.length + 1
                            ? 'active'
                            : 'pending'
                      }`}
                    >
                      {num}
                    </div>
                  ))}
                </div>
              </div>
              {gameState.turn_darts.length > 0 && (
                <div className="turn-darts">
                  <span className="label">This turn:</span>
                  <span className="darts-list">
                    {gameState.turn_darts.join(', ')}
                  </span>
                  <span className="turn-total">
                    (Total: {gameState.turn_darts.reduce((a, b) => a + b, 0)})
                  </span>
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {/* Players Scoreboard */}
      <div className="scoreboard">
        <h3>Players</h3>
        <div className="players-grid">
          {gameState.players.map((player, index) => (
            <div
              key={player.user_id}
              className={`player-card ${
                index === gameState.current_player_index ? 'active' : ''
              } ${player.status}`}
            >
              <div className="player-name">{player.user_id}</div>
              <div className="player-score">{player.score}</div>
              {player.busted && <div className="busted-badge">BUST</div>}
              {player.status === 'finished' && (
                <div className="finished-badge">✓ WON</div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Dartboard Grid */}
      {gameState.game_status === 'active' && (
        <div className="dartboard">
          <h3>Select Dart Value</h3>
          <div className="dart-grid">
            {/* Numbers 1-20 with single, double, triple */}
            {Array.from({ length: 20 }, (_, i) => i + 1).map((num) => (
              <div key={`group-${num}`} className="dart-group">
                <div className="group-number">{num}</div>
                <div className="dart-options">
                  <button
                    className={`dart-btn single ${
                      selectedDart === num ? 'selected' : ''
                    }`}
                    onClick={() => handleDartClick(num)}
                    disabled={!canPlayDarts || isLoading}
                    title={`Single ${num}`}
                  >
                    {num}
                  </button>
                  <button
                    className={`dart-btn double ${
                      selectedDart === num * 2 ? 'selected' : ''
                    }`}
                    onClick={() => handleDartClick(num * 2)}
                    disabled={!canPlayDarts || isLoading}
                    title={`Double ${num}`}
                  >
                    D
                  </button>
                  <button
                    className={`dart-btn triple ${
                      selectedDart === num * 3 ? 'selected' : ''
                    }`}
                    onClick={() => handleDartClick(num * 3)}
                    disabled={!canPlayDarts || isLoading}
                    title={`Triple ${num}`}
                  >
                    T
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Bullseye Row */}
          <div className="bullseye-section">
            <button
              className={`dart-btn outer-bull ${
                selectedDart === 25 ? 'selected' : ''
              }`}
              onClick={() => handleDartClick(25)}
              disabled={!canPlayDarts || isLoading}
              title="Outer Bull (25)"
            >
              25
            </button>
            <button
              className={`dart-btn bull ${selectedDart === 50 ? 'selected' : ''}`}
              onClick={() => handleDartClick(50)}
              disabled={!canPlayDarts || isLoading}
              title="Bull (50)"
            >
              50
            </button>
            <button
              className={`dart-btn miss ${selectedDart === 0 ? 'selected' : ''}`}
              onClick={() => handleDartClick(0)}
              disabled={!canPlayDarts || isLoading}
              title="Miss (0)"
            >
              MISS
            </button>
          </div>
        </div>
      )}

      {/* Game Messages */}
      {!canPlayDarts && gameState.game_status === 'active' && (
        <div className="info-message">
          Waiting for {currentPlayer?.user_id}'s turn...
        </div>
      )}

      {/* Turn History */}
      {gameState.history.length > 0 && (
        <div className="history">
          <h3>Turn History</h3>
          <div className="history-list">
            {gameState.history.map((turn, idx) => (
              <div key={idx} className={`history-item ${turn.busted ? 'bust' : ''}`}>
                <span className="turn-number">Turn {idx + 1}:</span>
                <span className="player-name">
                  {gameState.players[turn.player_index].user_id}
                </span>
                <span className="darts-thrown">{turn.darts.join(', ')}</span>
                <span className="scores">
                  {turn.start_score} → {turn.end_score}
                </span>
                {turn.busted && <span className="bust-label">BUST</span>}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default DartsBoard;
