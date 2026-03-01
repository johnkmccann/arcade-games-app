# MongoDB Schema Documentation

## Collections

### Users
- **Description**: Stores user information.
- **Fields**:
  - `username`: String, unique identifier for the user.
  - `email`: String, user's email address.
  - `password`: String, hashed password.

### Games
- **Description**: Stores information about the games.
- **Fields**:
  - `title`: String, title of the game.
  - `genre`: String, genre of the game.
  - `releaseDate`: Date, release date of the game.
  - `rating`: Number, game rating on a scale from 1 to 10.

### Scores
- **Description**: Stores user scores for different games.
- **Fields**:
  - `userId`: ObjectId, reference to the user.
  - `gameId`: ObjectId, reference to the game.
  - `score`: Number, score achieved by the user.
  - `dateAchieved`: Date, date when the score was achieved.