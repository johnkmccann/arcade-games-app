import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

const App = () => {
  return (
    <Router>
      <div>
        <header>
          <h1>Arcade Games App</h1>
        </header>
        <main>
          <Switch>
            {/* Define your routes here */}
            <Route path="/" exact>
              <h2>Home Page</h2>
            </Route>
            {/* Additional routes can be added here */}
          </Switch>
        </main>
        <footer>
          <p>&copy; 2026 Arcade Games. All rights reserved.</p>
        </footer>
      </div>
    </Router>
  );
};

export default App;