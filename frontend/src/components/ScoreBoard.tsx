import React from 'react';

const ScoreBoard: React.FC = () => {
    const [leaderboard, setLeaderboard] = React.useState<{ name: string; score: number }[]>([]);

    // Simulated leaderboard data
    React.useEffect(() => {
        const fetchLeaderboard = async () => {
            // Simulating a fetch from API
            const data = [
                { name: 'Player 1', score: 150 },
                { name: 'Player 2', score: 120 },
                { name: 'Player 3', score: 100 },
            ];
            setLeaderboard(data);
        };
        fetchLeaderboard();
    }, []);

    return (
        <div>
            <h1>Leaderboard</h1>
            <ul>
                {leaderboard.map((player, index) => (
                    <li key={index}>{player.name}: {player.score}</li>
                ))}
            </ul>
        </div>
    );
};

export default ScoreBoard;