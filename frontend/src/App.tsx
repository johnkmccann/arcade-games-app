import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import GameList from './components/GameList';
import { DartsSetup, DartsGame, DartsResults } from './games/darts';

const App = () => {
  return (
    <Router>
      <div>
        <header>
          <h1>Arcade Games App</h1>
        </header>
        <main>
          <Routes>
            {/* Game Discovery */}
            <Route path="/" element={<GameList />} />
            <Route path="/games" element={<GameList />} />

            {/* Darts Routes */}
            <Route path="/games/darts/start" element={<DartsSetup />} />
            <Route path="/games/darts/play/:sessionId" element={<DartsGame />} />
            <Route path="/games/darts/results/:sessionId" element={<DartsResults />} />

            {/* Additional routes can be added here */}
          </Routes>
        </main>
        <footer>
          <p>&copy; 2026 Arcade Games. All rights reserved.</p>
        </footer>
      </div>
    </Router>
  );
};

export default App;