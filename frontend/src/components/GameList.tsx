import React from 'react';

const games = [
    { id: 1, name: 'Chess', description: 'Classic chess game for two players.' },
    { id: 2, name: 'Sudoku', description: 'Number puzzle game.' },
    { id: 3, name: 'Pac-Man', description: 'Arcade game where you control Pac-Man through a maze.' },
    { id: 4, name: 'Tetris', description: 'Falling block puzzle game.' },
    // Add more games as needed
];

const GameList: React.FC = () => {
    return (
        <div>
            <h1>Available Games</h1>
            <ul>
                {games.map(game => (
                    <li key={game.id}>  
                        <h2>{game.name}</h2>
                        <p>{game.description}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default GameList;
