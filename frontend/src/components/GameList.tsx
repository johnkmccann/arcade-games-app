import React from 'react';
import { useNavigate } from 'react-router-dom';

const games = [
    { id: 1, name: 'Chess', description: 'Classic chess game for two players.', path: '/games/chess' },
    { id: 2, name: 'Sudoku', description: 'Number puzzle game.', path: '/games/sudoku' },
    { id: 3, name: 'Pac-Man', description: 'Arcade game where you control Pac-Man through a maze.', path: '/games/pacman' },
    { id: 4, name: 'Tetris', description: 'Falling block puzzle game.', path: '/games/tetris' },
    { id: 5, name: '🎯 Darts', description: 'Score tracking for physical dartboards. 2-8 players.', path: '/games/darts/start' },
    // Add more games as needed
];

const GameList: React.FC = () => {
    const navigate = useNavigate();

    const handleGameClick = (gamePath: string) => {
        navigate(gamePath);
    };

    return (
        <div>
            <h1>Available Games</h1>
            <ul>
                {games.map(game => (
                    <li key={game.id}>
                        <h2>{game.name}</h2>
                        <p>{game.description}</p>
                        <button onClick={() => handleGameClick(game.path)}>Play</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default GameList;
