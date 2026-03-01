import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

const App = () => {
  return (
    <Router>
      <div>
        <header>
          <h1>Arcade Games App</h1>
        </header>
        <main>
          <Routes>
            {/* Define your routes here */}
            <Route path="/" element={<h2>Home Page</h2>} />
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